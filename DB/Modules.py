from threading import Timer
import pandas as pd
import numpy as np
import pymysql

class Mysql:
  def __init__(self, host, user, password, db):
    #데이터베이스에 접속
    self.__host = host
    self.__user = user
    self.__password = password
    self.__db = db
    self.contentlist = []
    
  def _connectDB(self):
    self._conn = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__db, charset='utf8')

  def _disconnectDB(self):
    self._conn.commit()
    self._conn.close()
    
  def add(self, content):
    self.contentlist.append(content)
    
  def __del__(self):
    #DB 연결 해제
    if self._conn.open:
      self._conn.close()
    
class Updater(Mysql):
  
  def update(self):
    self._connectDB()
    for c in self.contentlist:
      c.update(self._conn)
    self._disconnectDB()
    
  def summary(self):
    print('---------------------------------------------------------------------------------------------')
    for c in self.contentlist:
      print(c.update_summary)
    print('---------------------------------------------------------------------------------------------')  
    
  def update_Timer(self, hour):
    """
    타이머 설정으로 지정된 시간마다 업데이트
    hour : 업데이트 할 시간 간격
    """
    print('Waiting for Update')
    self.update()
    t = Timer(3600 * hour, self.update)
    t.start()

class Reader(Mysql):
  
  def read(self):
    self._connectDB()
    output = []
    for c in self.contentlist:
      output.append(c.read(self._conn))
    self._disconnectDB()
    
    return output
  
  def summary(self):
    print('---------------------------------------------------------------------------------------------')
    for c in self.contentlist:
      print(c.read_summary)
    print('---------------------------------------------------------------------------------------------')  
