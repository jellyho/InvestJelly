import numpy as np
import importlib

class TimeSeries:
    def __init__(self, df, title=None):
        self.df = df
        self.columns = df.columns
        self.title = title

    def __del__(self):
        pass

    def __str__(self):
        return f'{self.title} : from {self.df.index[0]} to {self.df.index[-1]}, {len(self.df)} Rows'

    def __repr__(self):
        return f'{self.title} : from {self.df.index[0]} to {self.df.index[-1]}, {len(self.df)} Rows'

    def __getitem__(self, i):
        if i in self.columns:
            return self.df[i]
        elif i == 'df':
          return self.df
        elif i=='columns':
          return self.columns
        elif i =='title':
          return self.title
        else:
            return getattr(importlib.import_module('.Indicators', 'InvestJelly.Structures'),i)(self.df)
        
    def __getattr__(self, i):
        if i in self.columns:
            return self.df[i]
        elif i == 'df':
          return self.df
        elif i=='columns':
          return self.columns
        elif i =='title':
          return self.title
        else:
            return getattr(importlib.import_module('.Indicators', 'InvestJelly.Structures'),i)(self.df)

    def __len__(self):
        return len(self.df)