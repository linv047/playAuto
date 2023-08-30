#coding:utf-8
"""
author: baidu
time: 2021-07-26
describe：记录日志，并输出到控制台
"""
import logging
import os
from datetime import datetime
class Logger:

  def __init__(self):
    self.logger=logging.getLogger()
    self.logger.setLevel(logging.INFO)
    self.fomatter =logging.Formatter("%(asctime)s-[Line:%(lineno)s]-%(message)s")
  #设置控制台输出
    streamhandle=logging.StreamHandler()
    streamhandle.setFormatter(self.fomatter)
  #设置文件输出
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'log')
    self.file=os.path.join(log_path,datetime.now().strftime ("%Y_%m_%d") +".txt")
    file_handle=logging.FileHandler(self.file)
    file_handle.setFormatter(self.fomatter)
    if not self.logger.handlers:
      self.logger.addHandler(file_handle)
      self.logger.addHandler(streamhandle)

  def get_log(self):
     return self.logger

if __name__=='__main__':
    Logger().get_log().debug("test....")