import pandas as pd
from ...Structures import TimeSeries, Ohlcv

class tickers:
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
        df[i] = pd.read_sql(sql, _conn)[:][0]
    return TimeSeries(df, title=self._summary())
