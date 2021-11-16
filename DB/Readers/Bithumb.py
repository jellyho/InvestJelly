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
  ticker: 불러올 코인의 코드, random
  intervals: 불러올 거래 데이터 간격 []
  date: 불러올 데이터의 시작 날짜 %Y-%m-%d %H:%M:%S , random , latest
  amount: [] intervals 당 amount
  """
  def __init__(self, ticker='random', intervals='all', date='latest', amount=50):
    
    self.ticker = ticker
    
    if date == 'latest':
      self.date = datetime.now(timezone('Asia/Seoul'))[:19]
    else:
      self.date = date
      
    self.__interval_order = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h' ]
    
    if intervals == 'all':
      self.interval = self.__interval_order
      if type(amount) is int:
        self.amount = [amount for _ in range(len(self.__interval_order))]
      elif type(amount) is list and len(amount) == len(self.interval):
        self.amount = amount
      else:
        raise ValueError('amount is not fit with intervals')
    else:
      self.interval = intervals
      if type(amount) is int:
        self.amount = [amount for _ in range(len(intervals))]
      elif type(amount) is list and len(amount) == len(self.interval):
        self.amount = amount
      else:
        raise ValueError('amount is not fit with intervals')
    
    
      
  def _summary(self):
    return f'Bithumb ohlcv_krw {self.ticker}-{self.interval}-{self.amount} datas before {self.date}'
  
  def _read(self, _conn):
    
    def pickticker():
      if self.ticker == 'random':
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
        return code
    
    checked = False
    result = []
    while not checked:
      checked = True
      if self.ticker == 'random':
        self.ticker = pickticker()
        
      for i in range(len(self.interval)):
        with _conn.cursor() as curs:
          sql = f"SELECT * FROM bithumb_{self.interval[i]}_ohlcv ORDER BY date DESC WHERE code = '{self.ticker}' and date <= '{self.date}' LIMIT {self.amount[i]}"
          df = pd.read_sql(sql, _conn)
          if len(df) == self.amount[i]:
            df.index = df['date']
            df = df[['code', 'open', 'high', 'low', 'close', 'volume']]
            result.append(Ohlcv(df, title='Bitumb Ohlcv_krw {self.interval[i]} {self.ticker}, {len(df)} Rows'))
          elif self.ticker == 'random':
            checked = False
            break
          else:
            raise ValueError('Not enough {self.ticker}-{self.interval[i]} data')
            
    return result
