import datetime
import pybithumb
import pandas as pd

class ohlcv_krw:
    """
    빗썸 Public API를 이용하는 pybithumb 패키지를 이용하여 주기적으로 암호화폐의 거래정보를 다운로드, mysql 데이터베이스에 저장.
    """

    #DB에 데이터베이스 생성(첫 실행시)
    def __init__(self, intervals='all'):
        self.__interval_order = {
            '1m': datetime.timedelta(minutes=1),
            '3m': datetime.timedelta(minutes=3),
            '5m': datetime.timedelta(minutes=5),
            '10m': datetime.timedelta(minutes=10),
            '30m': datetime.timedelta(minutes=30),
            '1h': datetime.timedelta(hours=1),
            '6h': datetime.timedelta(hours=6),
            '12h': datetime.timedelta(hours=12),
            '24h': datetime.timedelta(days=1)
        }
        if intervals == 'all':
            self.interval = [
                '1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h'
            ]
        else:
            self.interval = intervals

    def _summary(self):
        return f'Bithumb ohlcv_krw {self.interval}'

    def _update(self, _conn):
        #업데이트 시작
        def checkdate(t, d):
          if t =='1m':
            return True
          elif t=='3m':
            return d.minute % 3 == 0
          elif t=='5m':
            return d.minute % 5 == 0
          elif t=='10m':
            return d.minute % 10 == 0
          elif t=='1h':
            return d.minute == 0
          elif t=='6h':
            return d.hour % 6 == 0
          elif t=='12h':
            return d.hour % 12 == 0
          else:
            return d.hour == 0
            
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
        print("Bithumb ohlcv_krw Update Started", datetime.datetime.today())
        #업데이트시 오류 생겨도 프로그램 종료 방지
        with _conn.cursor() as curs:
            for d in self.interval:
                #현재 빗썸에서 거래 가능한 코인 Ticker 목록을 받아옴.
                tickers = pybithumb.get_tickers('KRW')
                for t in tickers:
                    df = pybithumb.get_candlestick(t, 'KRW', d)[:-1]
                    print(
                        '\r                                                  ',
                        end="")
                    print(f'\rAdding {len(df)} rows of {d}_{t}',
                          end=" - ")

                    #DB업데이트 쿼리문
                    sql = f"REPLACE INTO bithumb_{d}_ohlcv (code, date, open, high, low, close, volume) VALUES "

                    for r in df.itertuples():
                        if checkdate(d, r.Index):
                          sql += f"('{t}', '{r.Index}', {r.open}, {r.high}, {r.low}, {r.close}, {r.volume}), "

                    sql = sql[:-2]
                    curs.execute(sql)
                    _conn.commit()
                    print('finished', end="")
                #업데이트 완료
        print("\rBithumb market_krw Update Finished,", datetime.datetime.today(),
              "                  ")
