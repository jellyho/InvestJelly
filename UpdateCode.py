from DB import Updater as u
from DB import Bithumb
updater = u('jellyho..ap-northeast-2.rds.amazonaws.com', 'admin', 'qlalfqjsgh1!', 'crypto')
updater.add(Bithumb.market_krw('all'))
updater.update_Timer(4)
