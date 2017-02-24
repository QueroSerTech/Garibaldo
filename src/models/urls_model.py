# -*- coding: UTF-8 -*-

from garibaldo_sqlite import Sqlite_Connection;

class UrlModel(object):

	def __init__(self):
		self.__connection = Sqlite_Connection().connection

	def insertUrl(self, data):
		