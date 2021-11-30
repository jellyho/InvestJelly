import numpy as np
import matplotlib.pyplot as plt

class Indicator:
  def __init__(self, df=None, **kwargs):
    if kwargs:
      self.kwargs=kwargs
    if df is not None:
      self.df = df
      if kwargs:
        self.df = self.method()

  def __call__(self, df=None, **kwargs):
    if kwargs:
      self.kwargs=kwargs
    if df is not None:
      self.df = df
      self.df = self.method()
    
    return self
  
  def label(self):
    return f'{self.__class__.__name__}'
  def method(self):
    return self.df

  def _plotsetting(self):
    return 'main'
    
  def draw(self, axs=None):
    if axs is not None:
      for c in self.df.columns:
        axs.plot(self.df.index, self.df[c], label=self.label()+"-"+c, lw=0.6)
    return self.df

class MA(Indicator):
  def method(self):
    window = self.kwargs['window']
    columns = self.kwargs['columns']

    return self.df.rolling(window=window).mean()[columns]

  def label(self):
    return f"MA{self.kwargs['window']}"

class BB(Indicator):
  def method(self):
    d = self.df.copy()
    d['std'] = d['close'].rolling(window=self.kwargs['window']).std()
    d['middle'] = d['close'].rolling(window=self.kwargs['window']).mean()
    d['upper'] = d['middle'] + (d['std'] * 2)
    d['lower'] = d['middle'] - (d['std'] * 2)
    d['pb'] = (d['close'] - d['lower']) / (d['upper'] - d['lower'])
    d['bw'] = (d['upper'] - d['lower']) / d['middle'] * 100

    d = d[['upper', 'lower', 'middle', 'pb', 'bw']]

    return d

  def draw(self, axs=None):
    if axs is not None:
      d = self.df
      axs.plot(d.index, d['middle'], lw = 0.6, zorder=10)
      axs.plot(d.index, d['upper'], label='BB upper', lw = 0.6, zorder=10)
      axs.plot(d.index, d['lower'], label='BB lower', lw = 0.6, zorder=10)
      axs.fill_between(d.index, d['upper'], d['lower'], alpha = 0.3)
    else:
      d = self.df
      plt.plot(d.index, d['middle'], lw = 0.6, zorder=10)
      plt.plot(d.index, d['upper'], label='BB upper', lw = 0.6, zorder=10)
      plt.plot(d.index, d['lower'], label='BB lower', lw = 0.6, zorder=10)
      plt.fill_between(d.index, d['upper'], d['lower'], alpha = 0.3)
      plt.show()

class MFI(Indicator):
  def _plotsetting(self):
    return 'sub'

  def method(self):
    d = self.df.copy()
    window = self.kwargs['window']
    d['tp'] = (d['high'] + d['low'] + d['close']) / 3
    d['pmf'] = 0
    d['nmf'] = 0
    for i in range(len(d.close) - 1):
        if d.tp.values[i] < d.tp.values[i + 1]:
            d.pmf.values[i +
                          1] = d.tp.values[i + 1] * d.volume.values[i + 1]
            d.nmf.values[i + 1] = 0
        else:
            d.nmf.values[i +
                          1] = d.tp.values[i + 1] * d.volume.values[i + 1]
            d.pmf.values[i + 1] = 0

    d['mfr'] = d.pmf.rolling(window=window).sum() / d.nmf.rolling(
        window=window).sum()

    d['mfi'] = 100 - 100 / (1 + d['mfr'])
    d = d['mfi']
    return d

class stch_RSI(Indicator):
  def _plotsetting(self):
    return 'sub'

  def method(self):
    d = self.df.copy()
    window = self.kwargs['window']
    max = d.high.rolling(window=window[0], min_periods=1).max()
    min = d.low.rolling(window=window[1], min_periods=1).min()
    pk = (d.close - min) / (max - min) * 100
    pd = pk.rolling(window=window[1]).mean()
    d['pk'] = pk
    d['pd'] = pd

    d = d[['pk', 'pd']]
    
    return d

class CCI(Indicator):
  def _plotsetting(self):
    return 'sub'

  def method(self):
    d = self.df.copy()
    window = self.kwargs['window']
    tp = (d['high'] + d['low'] + d['close']) / 3
    ma = tp.rolling(window=window).mean()
    de = (tp - ma)
    d['cci'] = de / (np.abs(de).rolling(window=window).mean() * 0.015)
    d = d['cci']
    return d