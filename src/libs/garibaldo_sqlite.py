# -*- coding: UTF-8 -*-

import sqlite3

class Sqlite_Connection(object):

	def __init__(self):
		self._connection = sqlite3.connect('garibaldo.db').cursor();

	@property	
	def connection:
		return self._connection

