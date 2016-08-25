#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database layer
#   Currently written for sqlite3, and only for keeping colors
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import sqlite3

from TIME.lib.Config import Configuration as conf

memDB = sqlite3.connect(":memory:")
realDB = conf.getPSQLConnection()

def _dbWrapped(funct):
  def wrapper(*args, **kwargs):
    if realDB:
      db =realDB
      cur=realDB.cursor()
    else:
      ensureDB()
      db =memDB
      cur=memDB.cursor()
    result = funct(db, cur, *args, **kwargs)
    cur.close()
    return result
  return wrapper

def _requiresRealDB(funct):
  def wrapper(*args, **kwargs):
    if not realDB: sys.exit("Could not reach the postgres database")

def ensureDB():
  memDB.execute('''CREATE TABLE IF NOT EXISTS Plugins
                  (Plugin_ID  INT      PRIMARY KEY,
                   Name       Text     UNIQUE,
                   Color      TEXT,
                   Size       INTEGER  DEFAULT 30);''')

############################################################################
# These functions are available for both the postgres db and the memory db #
############################################################################
@_dbWrapped
def add_plugin_info(db, curs, plugin, color, size = 30):
  curs.execute("""INSERT INTO Plugins(Name, Color, Size)
                  VALUES(?, ?, ?)""", (plugin, color, size))
  db.commit()

def get_plugins(plugin=None):
  where = ["Name='%s'"%plugin] if plugin else []
  p = selectAllFrom("Plugins", where)
  if plugin:
    return p[0] if len(p) is 1 else None
  else: return p

@_dbWrapped
def selectAllFrom(db, curs, table, where=None):
  wh="where "+" and ".join(where) if where else ""
  data=list(curs.execute("SELECT * FROM %s %s"%(table,wh)))
  dataArray=[]
  names = list(map(lambda x: x[0], curs.description))
  for d in data:
    j={}
    for i in range(0,len(names)):
      j[names[i].lower()]=d[i]
    dataArray.append(j)
  return dataArray
  
  
  
