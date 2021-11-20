from datetime import datetime
import pandas as pd
import numpy as np
import pybithumb
import pymysql


class ohlcv_krw:
  """
  빗썸 Public API를 이용하는 pybithumb 패키지를 이용하여 주기적으로 암호화폐의 거래정보를 다운로드, mysql 데이터베이스에 저장.
  """
  #DB에 데이터베이스 생성(첫 실행시)
  def __init__(self, intervals='all'):
    if intervals == 'all':
      self.interval = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h' ]
    else:
      self.interval = intervals
  
  def _summary(self):
    return f'Bithumb market_krw {self.interval}'
  
  def _update(self, _conn):
    #업데이트 시작
    with _conn.cursor() as curs:
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
    _conn.commit()
    print("Bithumb market_krw Update Started", datetime.today())
    #업데이트시 오류 생겨도 프로그램 종료 방지
    with _conn.cursor() as curs:
      for d in self.interval:
        try:
          #현재 빗썸에서 거래 가능한 코인 Ticker 목록을 받아옴.
          tickers = pybithumb.get_tickers('KRW')
          for t in tickers:
            try:
              sql = f"SELECT max(date) FROM bithumb_{d}_ohlcv WHERE code = '{t}'"
              curs.execute(sql)
              rs = curs.fetchone()
              df = pybithumb.get_candlestick(t, 'KRW', d)
              today = df.index[-1]
              #업데이트가 필요한지 판단.
              if rs[0] is None or rs[0] < today:
                if df is None:
                  continue
                #업데이트할 데이터만 남기고 제거.
                if not rs[0] is None:
                  df = df[rs[0]:]
                
                #가장 최근 데이터는 시간대가 정확하지 않으므로 제거.
                #df = df.drop(today)
                
                #업데이트 현황 프린트
                print('\r                                                  ',end="")
                print(f'\rAdding {len(df)} rows of {d}_{t}', end=" - ") 
                
                #DB업데이트 쿼리문
                sql = f"REPLACE INTO bithumb_{d}_ohlcv (code, date, open, high, low, close, volume) VALUES "
                
                for r in df.itertuples():
                  sql += f"('{t}', '{r.Index}', {r.open}, {r.high}, {r.low}, {r.close}, {r.volume}), "

                sql = sql[:-2]
                curs.execute(sql)
                _conn.commit()
                print('finished', end="")
            except Exception as e:
              print(f'Network Error')
        except Exception as e:
          print(f'Network Error')
        #업데이트 완료             
    print("\rBithumb market_krw Update Finished,", datetime.today(),"                  ")
