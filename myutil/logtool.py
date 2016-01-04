import os
import logging
class logtool(object):
	def __init__(self,logname,filehandle):
		self.__logger = logging.getLogger(logname)
		handler = logging.FileHandler(filehandle)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
		handler.setFormatter(formatter)
		self.__logger.addHandler(handler)
		self.__logger.setLevel(logging.INFO)
	def info(self,msg):
		self.__logger.info(msg)
	def debug(self,msg):
		self.__logger.log(msg)
	def debug(self,msg):
		self.__logger.error(msg)
if __name__ == '__main__':
	l=logtool('log1','log.txt')
	l.info('sssssssssssss')
