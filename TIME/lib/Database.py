#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Postgres Database
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import os
import psycopg2.extras
import sqlite3

from TIME.lib.Config import Configuration as conf

class PostgresDatabase():
  def __init__(self):
    self.db = conf.getPSQLConnection()
    if not self.db: raise(Exception)
    self.cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

  def add_plugin(self, plugin, color, size = 30):
    self.cur.execute("""INSERT INTO Plugins(Name, Color, Size)
                        SELECT %s, %s, %s
                        WHERE NOT EXISTS(
                          SELECT Name FROM Plugins WHERE Name = %s);""",
                        (plugin, color, size, plugin))
    self.db.commit()

  def get_plugins(self, plugin=None):
    statement = "SELECT * FROM Plugins"
    if plugin: statement += " WHERE Name = %s"
    self.cur.execute(statement, (plugin,))
    return self.cur.fetchall()

  def get_user(self, username):
    self.cur.execute("""SELECT * FROM Users
                        WHERE Username = %s LIMIT 1;""", (username,))
    return self.cur.fetchall()

  def teams_for_user(self, username):
    self.cur.execute("""SELECT * FROM Teams
                        WHERE Team_ID IN(
                          SELECT Team_ID FROM Users_In_Teams
                          WHERE User_ID IN(
                            SELECT User_ID FROM Users
                            WHERE Username = %s));""", (username,))
    return self.cur.fetchall()

  def cases_for_team(self, team):
    self.cur.execute("""SELECT * FROM Cases
                        WHERE Case_ID IN(
                          SELECT Case_ID FROM Case_Access
                          WHERE Team_ID IN(
                            SELECT Team_ID FROM Teams
                            WHERE Name = %s));""", (team,))
    return self.cur.fetchall()

class SQLITEDatabase():
  def __init__(self):
    import TIME.lib as lib
    self.db = sqlite3.connect(":memory:")
    self.cur = self.db.cursor()
    lib = os.path.dirname(os.path.realpath(lib.__file__))

    db_struct = open(os.path.join(lib, "db_model.sql")).read()
    for statement in db_struct.split(";"): self.cur.execute(statement+";")
    #self.db_data   = open(os.path.join(lib, "db_data.sql")).read()

  def add_plugin(self, plugin, color, size = 30):
    self.cur.execute("""INSERT INTO Plugins(Name, Color, Size)
                        Values(?, ?, ?);""", (plugin, color, size))
    self.db.commit()

  def get_plugins(self, plugin=None):
    where = ["Name='%s'"%plugin] if plugin else []
    return self._selectAllFrom("Plugins", where)

  def get_user(self, username):
    return self.cur.execute("SELECT * FROM Users WHERE username = %s", username)

  def _selectAllFrom(self, table, where=None):
    wh="where "+" and ".join(where) if where else ""
    data=list(self.cur.execute("SELECT * FROM %s %s"%(table,wh)))
    dataArray=[]
    names = list(map(lambda x: x[0], self.cur.description))
    for d in data:
      j={}
      for i in range(0,len(names)):
        j[names[i].lower()]=d[i]
      dataArray.append(j)
    return dataArray


