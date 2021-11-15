import pandas as pd
from random import randrange
from datetime import datetime
from pytz import timezone
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
  tickers: 불러올 코인의 코드, random
  intervals: 불러올 거래 데이터 간격 []
  date: 불러올 데이터의 시작 날짜 %Y-%m-%d %H:%M:%S , random , latest
  amount: [] intervals 당 amount
  """
  def __init__(self, tickers='random', intervals='all', date='latest', amount=50):
    
    self.tickers = tickers
    
    if date == 'latest':
      self.date = datetime.now(Timezone('Asia/Seoul'))
    else:
      self.date = date
      
    self.__interval_order = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h' ]
    
    if intervals == 'all':
      self.interval = self.__interval_order
      if type(amount) is int:
        self.amount = [amount for _ in range(len(intervals))]
      elif type(amount) is list and len(amount) == len(self.interval):
        self.amount = amount
      else:
        raise ValueError('amount data is not fit with intervals')
    else:
      self.interval = intervals
      if type(amount) is int:
        self.amount = [amount for _ in range(len(intervals))]
      elif type(amount) is list and len(amount) == len(self.interval):
        self.amount = amount
      else:
        raise ValueError('amount data is not fit with intervals')
    
    
      
  def _summary(self):
    return f'Bithumb ohlcv_krw {self.tickers}-{self.interval}-{self.amount} datas before {self.date}'
  
  def _read(self, _conn):
    
    if self.tickers == 'random':
      df = pd.DataFrame()
      with _conn.cursor() as curs:
        for i in self.interval:
          sql = f"SELECT DISTINCT code FROM bithumb_{i}_ohlcv"
          df[i] = pd.read_sql(sql, _conn).iloc[:,0].values
      checked = False
      while not checked:
        checked = True
        code = df[self.interval[0]][randrange(0,len(df[self.interval[0]]))]
        for i in self.interval:
          if code in df[i].values:
            continue
          else:
            checked = False
            break
      self.tickers = [code]
    return self.tickers
  
    
    """
    if start is None:
      with _conn.cursor() as curs:
        sql = f"SELECT min(date) FROM bithumb_{interval}_ohlcv WHERE code = '{code}'"
        curs.execute(sql)
        rs = curs.fetchone()
        start = datetime.strftime(rs[0], "%Y-%m-%d %H:%M:%S")

    if end is None:
      with _conn.cursor() as curs:
        sql = f"SELECT max(date) FROM bithumb_{interval}_ohlcv WHERE code = '{code}'"
        curs.execute(sql)
        rs = curs.fetchone()
        end = datetime.strftime(rs[0], "%Y-%m-%d %H:%M:%S")

    #데이터를 받아올 시작일과 마지막일 변환      
    start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    #데이터를 받아올 쿼리문
    sql = f"SELECT * FROM bithumb_{interval}_ohlcv WHERE code = '{code}' and date >= '{start}' and date <= '{end}'"
    df = pd.read_sql(sql, _conn)
    df.index = df['date']

    #데이터 가공
    df = df[['code', 'open', 'high', 'low', 'close', 'volume']]

    print(f'Bithumb Ohlcv_krw {interval} {code} from {df.index[0]} to {df.index[-1]}, {len(df)} Rows Loaded')

    return Ohlcv(df, title=f'Bithumb Ohlcv_krw {interval} {code}')
    """
