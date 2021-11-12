from datetime import datetime
from threading import Timer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pybithumb
import pymysql
import time
import re
import math

class BithumbDBUpdater:
    """
    빗썸 Public API를 이용하는 pybithumb 패키지를 이용하여 주기적으로 암호화폐의 거래정보를 다운로드, mysql 데이터베이스에 저장.
    """
    def __init__(self, host, user, password, db):
      #데이터베이스에 접속
      self.host = host
      self.user = user
      self.password = password
      self.db = db

    def __connectDB(self):
      self.__conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
      self.interval = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h' ]
      
      #DB에 데이터베이스 생성(첫 실행시)
      with self.__conn.cursor() as curs:
          for d in self.interval:
              sql = f"""
              create table if not exists bithumb_{d}_ohlcv (
              code VARCHAR(20),
              date TIMESTAMP,
              open DOUBLE(20, 4),
              high DOUBLE(20, 4),
              low DOUBLE(20, 4),
              close DOUBLE(20, 4),
              volume DOUBLE(20, 4),
              PRIMARY KEY (code, date)
              )
              """
              curs.execute(sql)
      self.__conn.commit()
    
    def __disconnectDB(self):
      self.__conn.commit()
      self.__conn.close()

    def __del__(self):
        #DB 연결 해제
        self.__conn.close()
 
    def Update(self):
        #업데이트 시작
        self.__connectDB();
        print("Update Start", datetime.today())
        
        #업데이트시 오류 생겨도 프로그램 종료 방지
        with self.__conn.cursor() as curs:
                for d in self.interval:
                    try:
                        sql = f"SELECT max(date) FROM bithumb_{d}_ohlcv"
                        curs.execute(sql)
                        rs = curs.fetchone()
                        today = datetime.today()
                        print('\r'+f'{d}                 ')
 
                        #업데이트가 필요한지 판단.
                        if rs[0] is None or rs[0] < today:
                          #현재 빗썸에서 거래 가능한 코인 Ticker 목록을 받아옴.
                          tickers = pybithumb.get_tickers('KRW')
                          for t in tickers:
                            try:
                              df = pybithumb.get_candlestick(t, 'KRW', d)
                              if df is None:
                                  continue

                              #가장 최근 데이터는 시간대가 정확하지 않으므로 제거.
                              df = df.drop(df.index[-1])

                              #업데이트할 데이터만 남기고 제거.
                              if not rs[0] is None:
                                  df = df[rs[0]:]
                              #DB업데이트 쿼리문
                              #업데이트 현황 프린트
                              print('\r'+f'{t}           ', end="") 
                              for r in df.itertuples():
                                sql = f"""
                                      REPLACE INTO bithumb_{d}_ohlcv VALUES ('{t}', '{r.Index}', {r.open}, {r.high}, {r.low}, {r.close}, {r.volume})
                                      """
                                curs.execute(sql)
                              self.__conn.commit()

                              #과도한 API사용으로 API사용 정지 하지 않도록 속도 조절 (초당 20회 이하로 이용)
                              time.sleep(1 / 100) 
                            except Exception as e:
                              print(f'{d}-{t} 업데이트 중 네트워크 오류 발생')  
                    except Exception as e:
                        print(f'{d} 업데이트 중 네트워크 오류 발생')
 
        #업데이트 완료             
        print("Update Finished,", datetime.today())
        self.__disconnectDB()

    def Update_Timer(self, hour):
        """
        타이머 설정으로 지정된 시간마다 업데이트
        hour : 업데이트 할 시간 간격
        """
        self.Update()
        t = Timer(3600 * hour, self.Update_Timer)
        t.start()
