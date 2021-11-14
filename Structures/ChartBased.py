class TimeSeries:
  def __init__(self, df, title=None):
    self.df = df
    self.columns = df.columns
    self.title = title

  def __del__(self):
    pass

  def __str__(self):
    return f'{self.title} : from {self.df.index[0]} to {self.df.index[-1]}, {len(self.df)} Rows'

  def MA(self, window, columns=None):
    """
    Moving Average
    window: window
    """
    if columns is None:
      return self.df.rolling(window=window).mean()
    else:
      return self.df[columns].rolling(window=window).mean()

class Ohlcv(TimeSeries):
  def BB(self, window):
    """
    볼린저 밴드 가져오기 
    window: 이동평균 크기
    """
    d = self.df.copy()
    d['std'] = d['close'].rolling(window=window).std()
    d['middle'] = self.MA(['close'], window)
    d['upper'] = d['middle'] + (d['std'] * 2)
    d['lower'] = d['middle'] - (d['std'] * 2)
    d['pb'] = (d['close'] - d['lower']) / (d['upper'] - d['lower'])
    d['bw'] = (d['upper'] - d['lower']) / d['middle'] * 100

    d = d[['upper', 'lower', 'pb', 'bw']]

    return d

  def MFI(self, window):
    d = self.df.copy()
    d['tp'] = (d['high'] + d['low'] + d['close']) / 3
    d['pmf'] = 0
    d['nmf'] = 0
    for i in range(len(d.close)-1):
      if d.tp.values[i] < d.tp.values[i+1]:
        d.pmf.values[i+1] = d.tp.values[i+1] * d.volume.values[i+1]
        d.nmf.values[i+1] = 0
      else:
        d.nmf.values[i+1] = d.tp.values[i+1] * d.volume.values[i+1]
        d.pmf.values[i+1] = 0
          
    d['mfr'] = d.pmf.rolling(window=window).sum() / d.nmf.rolling(window=window).sum()
    
    d['mfi'] = 100 - 100 / (1 + d['mfr'])
    d = d['mfi']
    return d

  def stch_RSI(self, window):
    """
    스토캐스틱 RSI
    window = [highwindow, lowwindow]
    """
    d = self.df.copy()
    max = d.high.rolling(window=window[0], min_periods=1).max()
    min = d.low.rolling(window=window[1], min_periods=1).min()
    pk = (d.close - min) / (max - min) * 100
    pd = pk.rolling(window=window[1]).mean()
    d['pk'] = pk
    d['pd'] = pd

    d = d[['pk', 'pd']]
    return d

  def CCI(self, df, window):
    d = self.df.copy()
    tp = (d['high'] + d['low'] + d['close']) / 3
    ma = tp.rolling(window=window).mean()
    de = (tp - ma)
    d['cci'] = de / (np.abs(de).rolling(window=window).mean() * 0.015)
    d = d['cci']
    return d
