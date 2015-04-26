#!/usr/bin/python
#coding: utf8
import tarfile, os, sys, sqlite3

with tarfile.open('mod_blank.tgz', "w:gz") as tar:
	tar.add('mod_$LOW_NAME$', arcname=os.path.basename('mod_$LOW_NAME$'))

db_filename = r"settings.db"
db_is_new = not os.path.exists(db_filename)
conn = sqlite3.connect(db_filename)
cursor = conn.cursor() 
if db_is_new:
	print 'Need to create schema'
	dataTableCreation = """
					CREATE TABLE data (
						id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
						File BLOB,
						Type TEXT,
						FileName TEXT
					);
					"""
	infoTableCreation = """ 
					CREATE TABLE userinfo (
						id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
						name TEXT,
						email TEXT,
						site TEXT,
						lang TEXT,
						moduleDir TEXT
					);
					"""
	conn.execute(dataTableCreation)
	conn.execute(infoTableCreation)
	conn.commit()
else:
	print 'Database exists, assume schema does, too.'

tgzFile = r"mod_blank.tgz"
cursor.execute("DELETE FROM userinfo")
cursor.execute("VACUUM")
cursor.execute("INSERT INTO userinfo (name,email,site,lang) VALUES('Nikolay Shangin','shanginn@gmail.com','http://vk.com/shangin74','ru-RU')") 

with open(tgzFile, "rb") as input_file:
	ablob = input_file.read() 
	cursor.execute("DELETE FROM data")
	cursor.execute("VACUUM")
	cursor.execute("INSERT INTO data (File,Type,FileName) VALUES(?,'module','" + tgzFile + "')", [sqlite3.Binary(ablob)]) 
	conn.commit()