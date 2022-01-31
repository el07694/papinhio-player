import sqlite3
from sqlite3 import Error
import sys
sys.path.append("..")

def create_connection(db_file):
	""" create a database connection to a SQLite database """
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

			

def create_database_file():
	conn = create_connection("../database.db")
	cur = conn.cursor()

	db_file = open("tables.sql","r",encoding='utf-8')
	db_contents = db_file.read()
	db_commands = db_contents.split(";")

	for sql_command in db_commands[1:-2]:
		cur.execute(sql_command)
		conn.commit()
	conn.close()