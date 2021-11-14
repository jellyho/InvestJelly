import pandas as pd
import ..Structures import TimeSeries, Ohlcv
class tickers:
  def __init__(self, intervals):
    if intervals == 'all':
      self.interval = ['1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h' ]
    else:
      self.interval = intervals
  
  def _read(self, _conn):
    df = pd.DataFrame()
    with self._conn.cursor() as curs:
      for i in self.interval:
        sql = f"SELECT DISTINCT code FROM bithumb_{i}_ohlcv"
        df[i] = pd.read_sql(sql, self._conn)
    return TimeSeries(df)
    
