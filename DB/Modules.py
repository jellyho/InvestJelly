from datetime import datetime
from threading import Timer
import pandas as pd
import numpy as np
import pybithumb
import pymysql

class Mysql:
  def __init__(self, host, user, password, db):
    #데이터베이스에 접속
    self.__host = host
    self.__user = user
    self.__password = password
    self.__db = db

  def connectDB(self):
    self._conn = pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__db, charset='utf8')

  def disconnectDB(self):
    self._conn.commit()
    self._conn.close()

  def __del__(self):
    #DB 연결 해제
    self._conn.close()
