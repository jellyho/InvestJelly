from InvestJelly.DB import Updater
from InvestJelly.DB import Reader
from InvestJelly.DB.Updaters import Bithumb as BD
from InvestJelly.DB.Readers import Bithumb as BR
from InvestJelly.Visual.Chart import Visualizer

#u = Updater('jellyho.cyeickq2ncom.ap-northeast-2.rds.amazonaws.com', 'admin', 'qlalfqjsgh1!', 'crypto')
r = Reader('jellyho.cyeickq2ncom.ap-northeast-2.rds.amazonaws.com', 'admin', 'qlalfqjsgh1!', 'crypto')

r.add(BR.ohlcv_krw('random', 'all','random', amount=100))

result = r.read()[0]

vs = Visualizer.SimplePlot(result[0].df)