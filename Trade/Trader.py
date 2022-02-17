import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from enum import Enum

class Action(Enum):
  HOLD = 0
  BUY = 1
  SELL = 2
  LONG = 3
  CLOSE_LONG = 4
  SHORT = 5
  CLOSE_SHORT = 6

class Trader:
  def __init__(self, Env=None, Agent=None, Port=None):
    self.Env = Env
    self.Agent = Agent
    self.Portfolio = Port if Port else Portfolio()
    self.TradeHistory = TradeHistory()

  def method_Buy(self, TI):#
    return TI
  
  def method_Sell(self, TI):#
    return TI

  def method_Long(self, TI):#
    return TI

  def method_Short(self, TI):#
    return TI

  def Buy(self, ti):
    ti = self.method_Buy(ti)
    ti = self.Portfolio.add(ti)
    self.TradeHistory.append(ti)
    return None

  def Sell(self, ti):
    ti = self.method_Sell(ti)
    ti =  self.Portfolio.add(ti)
    self.TradeHistory.append(ti)
    return None

  def Long(self, ti):
    ti = self.method_Long(ti)
    ti =  self.Portfolio.add(ti)
    self.TradeHistory.append(ti)
    return None
  
  def Close_Long(self, ti):
    ti = self.method_Long(ti)
    ti =  self.Portfolio.add(ti)
    self.TradeHistory.append(ti)
    return None

  def Short(self, ti):
    ti = self.method_Short(ti)
    ti = self.Portfolio.add(ti)
    self.TradeHistory.append(ti)
    return None
  
  def Close_Short(self, ti):
    ti = self.method_Short(ti)
    ti = self.Portfolio.add(ti)
    self.TradeHistory.append(ti)
    return None
    
class TradeInfo:
  def __init__(self):
    self.df = pd.DataFrame(columns = ['Time', 'Action', 'Code', 'Amount', 'Price', 'Fee', 'Yield'])
    self.current = 0

  def __str__(self):
    return "\nTradeInfo\n" + str(self.df)
  
  def __getitem__(self, index):
    if index >= len(self.df):
      raise IndexError
    else:
      return self.df.iloc[index]

  def __iter__(self):
    return self         
 
  def __next__(self):
    if self.current < len(self.df):
      r = self.current
      self.current = self.current + 1
      return self.df.iloc[r]            
    else:                           
      raise StopIteration

  def append(self, Time, Action, Code, Amount, Price, Fee=0):
    self.df = self.df.append(pd.DataFrame({'Time':Time, 'Action':Action, 'Code':str(Code), 'Amount':float(Amount), 'Price':float(Price), 'Fee':float(Fee)}, index=[len(self.df)]))

class Portfolio:
  def __init__(self):
    self.Initial = self.set_Initial()
    self.Cash = self.Initial
    self.Yield = 0.00
    self.Value = self.Initial
    self.Ports = pd.DataFrame(columns = ['Code', 'Action', 'SPrice', 'Amount', 'CPrice', 'Yield'])

  def set_Initial(self):#
    return 1000000
  
  def load_Cash(self):#
    return self.Cash

  def cal_Port_Yields(self):
    bidx = (self.Ports['Action'] == Action.SHORT)
    for idx in bidx.index:
      if bidx[idx]:
        self.Ports['Yield'][idx] = (self.Ports['SPrice'][idx] - self.Ports['CPrice'][idx]) / self.Ports['CPrice'][idx] * 100
    
    bidx = (self.Ports['Action'] != Action.SHORT)
    for idx in bidx.index:
      if bidx[idx]:
        self.Ports['Yield'][idx] = (self.Ports['CPrice'][idx] - self.Ports['SPrice'][idx]) / self.Ports['SPrice'][idx] * 100

  def cal_Yield(self):
    self.Yield = (self.Value - self.Initial) / self.Value * 100

  def cal_Value(self):
    self.Value = (self.Ports['CPrice'] * self.Ports['Amount']).sum() + self.Cash

  def update(self, ObservedData=None):
    if ObservedData:
      self.update_Prices(ObservedData)
    self.cal_Port_Yields()
    self.load_Cash()
    self.cal_Value()
    self.cal_Yield()

  def update_Prices(self, ObservedData):#
    pass

  def __str__(self):
    return f'\nPortFolio Cash:{self.Cash}, Yield:{round(self.Yield,2)}%, Total Value:{self.Value}\n' + str(self.Ports)
    
  def add(self, TI):
    for t in TI:

      if t.Action in [Action.BUY, Action.LONG, Action.SHORT]:#구매
        self.Cash = self.Cash - t.Amount * t.Price

        if t.Code in list(self.Ports['Code']):#이미 포트에 있는 경우 추매로 판정
          codes = self.Ports[self.Ports['Code']==t.Code]
          if t.Action in list(codes['Action']):#평단가 조정
            targetidx = self.Ports[(self.Ports['Action']==t.Action) & (self.Ports['Code']==t.Code)].index.tolist()[0]
            before = self.Ports.loc[targetidx]['SPrice'] * self.Ports.loc[targetidx]['Amount']
            now = t.Amount * t.Price
            total = t.Amount + self.Ports.loc[targetidx]['Amount']
            self.Ports['SPrice'][targetidx] = ((before + now) / total)
            self.Ports['Amount'][targetidx] = total
        else:#포트에 없는 경우 새로 추가
          self.Ports = self.Ports.append(pd.DataFrame({'Code':t.Code, 'Action':t.Action, 'SPrice':t.Price, 'Amount':t.Amount, 'CPrice':t.Price, 'Yield':0.00},index=[len(self.Ports)]))

      elif t.Action in [Action.SELL, Action.CLOSE_LONG, Action.CLOSE_SHORT]:#판매
        if t.Action != Action.CLOSE_SHORT:
          self.Cash = self.Cash + t.Amount * t.Price
        if t.Code in list(self.Ports['Code']):#이미 포트에 있는 경우
          codes = self.Ports[self.Ports['Code']==t.Code]
          if Action(t.Action.value-1) in list(codes['Action']):#해당 amount 줄이기
            targetidx = self.Ports[(self.Ports['Action']==Action(t.Action.value-1)) & (self.Ports['Code']==t.Code)].index.tolist()[0]
            
            if t.Action == Action.CLOSE_SHORT:
              self.Cash = self.Cash + t.Amount * (2 * self.Ports['SPrice'][targetidx] - t.Price)
              TI.df['Yield'][TI.current-1] = (self.Ports['SPrice'][targetidx] - t.Price) / t.Price * 100
            else:
              TI.df['Yield'][TI.current-1] = (t.Price - self.Ports['SPrice'][targetidx]) / self.Ports['SPrice'][targetidx] * 100

            self.Ports['Amount'][targetidx] = self.Ports['Amount'][targetidx] - t.Amount

            if self.Ports['Amount'][targetidx] == 0:
              self.Ports = self.Ports.drop(targetidx)
      else:#무효 TradeInfo가 들어왔을 때
        pass
    self.update()
    return TI


class TradeHistory(TradeInfo):
  def __init__(self):
    self.df = pd.DataFrame(columns = ['Time', 'Action', 'Code', 'Amount', 'Price', 'Fee', 'Yield'])
    self.current = 0

  def __str__(self):
    return "\nTradeHistory\n" + str(self.df)

  def append(self, ti):
    self.df = self.df.append(ti.df)

  def closed(self):
    return self.df[(self.df['Action'] == Action.SELL) | (self.df['Action'] == Action.CLOSE_LONG) | (self.df['Action'] == Action.CLOSE_SHORT)]