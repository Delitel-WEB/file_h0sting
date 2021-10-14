# -*- coding: utf-8 -*-
# Created by Delitel

import sqlite3


class SQLither:

	def __init__(self, database):

		self.conn = sqlite3.connect(database)
		self.c = self.conn.cursor()

		self.c.execute("""CREATE TABLE IF NOT EXISTS users
			(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, status TEXT)""")
		self.c.execute("""CREATE TABLE IF NOT EXISTS admins
				(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER)""")
		self.c.execute("""CREATE TABLE IF NOT EXISTS user_files
				(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, file_id TEXT, time_upload TEXT, file_name TEXT, access TEXT, format TEXT, link TEXT)""")
		self.c.execute('''CREATE TABLE IF NOT EXISTS deletions_messages
				(user_id INTEGER, message_id INTEGER)''')
		self.c.execute("""CREATE TABLE IF NOT EXISTS some_people_succes
				(file_id INTEGER, people_ids TEXT)""")

	def exists_user_id(self, user_id):
		return bool(self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall())

	def exists_admin(self, user_id):
		return bool(self.c.execute("SELECT * FROM admins WHERE user_id=?", (user_id,)).fetchall())

	def add_user_id(self, user_id):
		self.c.execute("INSERT INTO users ('user_id', 'status') VALUES(?,?)", (user_id, 0,))
		self.conn.commit()

	def set_status(self, user_id, status):
		self.c.execute("UPDATE users SET status=? WHERE user_id=?", (status, user_id,))
		self.conn.commit()

	def get_files(self, user_id):
		return self.c.execute("SELECT * FROM user_files WHERE user_id=?", (user_id,)).fetchall()

	def get_status(self, user_id):
		return self.c.execute("SELECT status FROM users WHERE user_id=?", (user_id,)).fetchone()

	def get_deletions_messages(self, user_id):
		return self.c.execute("SELECT * FROM deletions_messages WHERE user_id=?", (user_id,)).fetchall()

	def delete_deletions_message(self, message_id):
		self.c.execute("DELETE FROM deletions_messages WHERE message_id=?", (message_id,))
		self.conn.commit()

	def add_delete_message(self, user_id, message_id):
		self.c.execute("INSERT INTO deletions_messages VALUES(?,?)", (user_id, message_id,))
		self.conn.commit()

	def add_file(self, user_id, file_id, time_upload, file_name, form, link):
		self.c.execute("INSERT INTO user_files ('user_id', 'file_id', 'time_upload', 'file_name', 'access', 'format', 'link') VALUES(?,?,?,?,?,?,?)", (user_id, file_id, time_upload, file_name, "nobody", form, link))
		self.conn.commit()

	def get_file(self, user_id, id_):
		return self.c.execute("SELECT * FROM user_files WHERE user_id=? and file_id=?", (user_id, id_,)).fetchone()

	def get_file_byID(self, id_):
		return self.c.execute("SELECT * FROM user_files WHERE id=?", (id_,)).fetchone()

	def update_access_data(self, id_, access):
		self.c.execute("UPDATE user_files SET access=? WHERE id=?", (access, id_,))
		self.conn.commit()

	def update_name_file(self, id_, file_name):
		self.c.execute("UPDATE user_files SET file_name=? WHERE id=?", (file_name, id_,))
		self.conn.commit()

	def delete_file(self, id_):
		self.c.execute("DELETE FROM user_files WHERE id=?", (id_,))
		self.conn.commit()

	def get_file_byLink(self, link):
		return self.c.execute("SELECT * FROM user_files WHERE link=?", (link,)).fetchone()

	def update_link(self, id_, link):
		self.c.execute("UPDATE user_files SET link=? WHERE id=?", (link, id_,))
		self.conn.commit()

