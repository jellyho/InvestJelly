import pandas as pd
from random import randrange
import datetime
from ...Structures import TimeSeries


class tickers_krw:
    def __init__(self, intervals):
        if intervals == 'all':
            self.interval = [
                '1m', '3m', '5m', '10m', '30m', '1h', '6h', '12h', '24h'
            ]
        else:
            self.interval = intervals

    def _summary(self):
        return f'Bithumb tickers {self.interval}'

    def _read(self, _conn):
        df = pd.DataFrame()
        with _conn.cursor() as curs:
            for i in self.interval:
                sql = f"SELECT DISTINCT code FROM bithumb_{i}_ohlcv"
                df[i] = pd.read_sql(sql, _conn).iloc[:, 0].values
        return df


class ohlcv_krw:
    """
  기간 입력 안되었을 때 최소 일자, 최대 일자로 초기화 됨
  ticker: 불러올 코인의 코드, random
  intervals: 불러올 거래 데이터 간격 []
  date: 불러올 데이터의 시작 날짜 %Y-%m-%d %H:%M:%S , random , latest
  amount: [] intervals 당 amount
  """
    def __init__(self,
                 ticker='random',
                 intervals='all',
                 _date='latest',
                 amount=50):

        self.ticker = ticker
        self.date = _date

        self.__interval_order = {
            '1m': datetime.timedelta(minutes=1),
            '3m': datetime.timedelta(minutes=3),
            '5m': datetime.timedelta(minutes=5),
            '10m': datetime.timedelta(minutes=10),
            '30m': datetime.timedelta(minutes=30),
            '1h': datetime.timedelta(hours=1),
            '6h': datetime.timedelta(hours=6),
            '12h': datetime.timedelta(hours=12),
            '24h': datetime.timedelta(days=1)
        }

        if intervals == 'all':
            self.interval = list(self.__interval_order.keys())
            if type(amount) is int:
                self.amount = [
                    amount for _ in range(len(self.__interval_order))
                ]
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
        return f'Bithumb ohlcv_krw {self.ticker}-{self.interval}-{self.amount} Rows before {self.date}'

    def _read(self, _conn):
        def pickticker():
            if self.ticker == 'random':
                df = pd.DataFrame()
                with _conn.cursor() as curs:
                    sql = ""
                    for i in range(len(self.interval)):
                        sql = f"SELECT DISTINCT code FROM bithumb_{self.interval[i]}_ohlcv"
                        df[self.interval[i]] = pd.read_sql(sql, _conn)['code']
                checked = False
                while not checked:
                    checked = True
                    code = df[self.interval[0]][randrange(
                        0, len(df[self.interval[0]]))]
                    for i in self.interval:
                        if code in df[i].values:
                            continue
                        else:
                            checked = False
                            break
                return code
            else:
                return self.ticker

        def tostr(data):
            return datetime.datetime.strftime(data, '%Y-%m-%d %H:%M:%S')

        def pickdate(ti):
            val = self.__interval_order['24h']
            i = '24h'

            #제일 우선순위 높은 interval 구하기
            for j in self.interval:
                off = self.__interval_order[j]
                if off <= val:
                    val = off
                    i = j
            for j in range(len(self.interval)):
                if self.interval[j] == i:
                    i = j

            sql = f"SELECT date FROM bithumb_{self.interval[i]}_ohlcv WHERE code = '{ti}'"
            df = pd.read_sql(sql, _conn)
            if len(df) >= self.amount[i]:
                df = df.iloc[self.amount[i]:, :]
                if self.date == 'latest':
                    return (df['date'][df.index[-1]])
                elif self.date == 'random':
                    return (df['date'][df.index[randrange(0, len(df))]])
                else:
                    if datetime.datetime.strptime(self.date,
                                         '%Y-%m-%d %H:%M:%S') in df['date']:
                        return self.date
                    else:
                        if self.ticker == 'random':
                            return False
                        else:
                            raise ValueError(
                                f'Not Enough {self.ticker} Data around {self.date}'
                            )
            else:
                if self.ticker == 'random':
                    return False
                else:
                    raise ValueError(f'Not Enough {self.ticker} Data')

        checked = False
        result = []
        interratio = 0.95
        while not checked:
            checked = True

            code = pickticker()
            res = pickdate(code)
            if res:
                for i in range(len(self.interval)):
                    ser = res - self.__interval_order[self.interval[i]] * self.amount[i]
                    sql = f"SELECT * FROM bithumb_{self.interval[i]}_ohlcv WHERE code = '{code}' and date <= '{tostr(res)}' and date > '{tostr(ser)}' ORDER BY date DESC"
                    df = pd.read_sql(sql, _conn).iloc[::-1, :]
                    df.index = df['date']
                    df = df[[
                        'code', 'open', 'high', 'low', 'close', 'volume'
                    ]]
                    if len(df) == self.amount[i]:
                        result.append(
                            TimeSeries(df, title=f"{code}-{self.interval[i]}"))
                    elif len(df) >= self.amount[i] * interratio:#보간
                      """
                      reseconds = int(datetime.datetime.strftime(res,'%s'))
                      divseconds = int(self.__interval_order[self.interval[i]].total_seconds())
                      res = reseconds - reseconds % (divseconds)
                      res = datetime.datetime.fromtimestamp(res)
                      order = [res - (self.__interval_order[self.interval[i]]) * j for j in range(self.amount[i])]
                      ordf = pd.DataFrame(index=order)

                      missing = []

                      for o in ordf.index:
                        if o not in df.index:
                          missing.append(o)
                      
                      tempdf = pd.DataFrame(index=missing,data={'code':code})

                      df = pd.concat([df, tempdf])
                      df = df.sort_index()
                      df = df.interpolate(method='time')
                      print(f'{len(missing)} Rows Missed, Interpolated')
                      """
                      result.append(
                            TimeSeries(df, title=f"{code}-{self.interval[i]}"))
                    elif self.ticker=='random' or self.date=='random':
                      checked = False
                      break
                    else:
                      raise ValueError('Too Many Missing Rows')
            else:
                checked = False
                result = []

        return result
