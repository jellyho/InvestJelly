import pandas as pd
from ..Structures import TimeSeries
pd.options.mode.chained_assignment = None

class Environment:
  def __init__(self):
    self.reset()
    
  def get_trade_fee(self):#
    return 0

  def get_tax_rate(self):#
    return 0

  def get_Data(self):#
    self.ObserveLength = 50
    return None

  def reset(self):
    self.trade_fee = self.get_trade_fee()
    self.tax_rate = self.get_tax_rate()
    self.Data = self.get_Data()
    self.idx = self.ObserveLength - 2

  def Observable(self):
    return (len(self.Data) - 1 > self.idx)

  def Observe(self):
    if self.Observable():
      self.idx = self.idx + 1
      return TimeSeries(df=self.Data[(self.idx-self.ObserveLength+1):(self.idx+1)])