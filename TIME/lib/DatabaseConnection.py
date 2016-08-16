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

path = ":memory:"
db=sqlite3.connect(path)

def _dbWrapped(funct):
    def wrapper(*args, **kwargs):
      ensureDB()
      result = funct(*args, **kwargs)
      return result
    return wrapper

def ensureDB():
  db.execute('''CREATE TABLE IF NOT EXISTS Plugins
                (Plugin  Text     PRIMARY KEY,
                 Color   TEXT,
                 Size    INTEGER  DEFAULT 30);''')

##############
# Store data #
##############
# Plugins
@_dbWrapped
def add_plugin_info(plugin, color, size = 30):
  db.execute("""INSERT OR REPLACE INTO Plugins(Plugin, Color, Size)
                VALUES(?, ?, ?)""", (plugin, color, size))
  db.commit()

##############
# Fetch data #
##############
# Plugins
def get_plugins(plugin=None):
  where = ["Plugin='%s'"%plugin] if plugin else []
  p = selectAllFrom("Plugins", where)
  if plugin:
    return p[0] if len(p) is 1 else None
  else: return p

@_dbWrapped
def selectAllFrom(table, where=None):
  curs=db.cursor()
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
  
  
  
