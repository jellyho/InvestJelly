from InvestJelly.DB import Updater
from InvestJelly.DB import Reader
from InvestJelly.DB.Updaters import Bithumb as BD
from InvestJelly.DB.Readers import Bithumb as BR

u = Updater('jellyho.cyeickq2ncom.ap-northeast-2.rds.amazonaws.com', 'admin', 'qlalfqjsgh1!', 'crypto')
r = Reader('jellyho.cyeickq2ncom.ap-northeast-2.rds.amazonaws.com', 'admin', 'qlalfqjsgh1!', 'crypto')

r.add(BR.ohlcv_krw('random', 'all', 'latest', amount=100))

result = r.read()[0][3]['close']

print(result)