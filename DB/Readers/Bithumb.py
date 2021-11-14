import pandas as pd
from ...Structures import TimeSeries, Ohlcv

class tickers_krw:
  def __init__(self, intervals):
    if intervals == 'all':
      self.interval = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h' ]
    else:
      self.interval = intervals
  def _summary(self):
    return f'Bithumb tickers {self.interval}'
  
  def _read(self, _conn):
    df = pd.DataFrame()
    with _conn.cursor() as curs:
      for i in self.interval:
        sql = f"SELECT DISTINCT code FROM bithumb_{i}_ohlcv"
        df[i] = pd.read_sql(sql, _conn).iloc[:,0].values
    return df

class ohlcv_krw:
    """
    기간 입력 안되었을 때 최소 일자, 최대 일자로 초기화 됨
    code: 불러올 코인의 코드
    interval: 불러올 거래 데이터 간격
    start: 불러올 데이터의 시작 날짜 %Y-%m-%d %H:%M:%S
    """
    self._connectDB()
    if start is None:
      with self._conn.cursor() as curs:
        sql = f"SELECT min(date) FROM bithumb_{interval}_ohlcv WHERE code = '{code}'"
        curs.execute(sql)
        rs = curs.fetchone()
        start = datetime.strftime(rs[0], "%Y-%m-%d %H:%M:%S")

    if end is None:
      with self._conn.cursor() as curs:
        sql = f"SELECT max(date) FROM bithumb_{interval}_ohlcv WHERE code = '{code}'"
        curs.execute(sql)
        rs = curs.fetchone()
        end = datetime.strftime(rs[0], "%Y-%m-%d %H:%M:%S")

    #데이터를 받아올 시작일과 마지막일 변환      
    start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    #데이터를 받아올 쿼리문
    sql = f"SELECT * FROM bithumb_{interval}_ohlcv WHERE code = '{code}' and date >= '{start}' and date <= '{end}'"
    df = pd.read_sql(sql, self._conn)
    df.index = df['date']

    #데이터 가공
    df = df[['code', 'open', 'high', 'low', 'close', 'volume']]

    print(f'Loaded {interval} {code} Data from {df.index[0]} to {df.index[-1]}, {len(df)} Rows')
    self._disconnectDB()

    return df
