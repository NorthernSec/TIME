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
    lib = os.path.dirname(os.path.realpath(lib.__file__))
    try:
      database = conf.getSQLITEPath()
      make_data = False if os.path.isfile(database) else True
      self.db = sqlite3.connect(database)
      self.cur = self.db.cursor()

      db_struct = open(os.path.join(lib, "db_model.sql")).read()
      for s in db_struct.split(";"): self.cur.execute(s+";")
      if make_data:
        db_data   = open(os.path.join(lib, "db_data.sql")).read()
        for s in db_data.split(";"): self.cur.execute(s+";")
    except Exception as e:
      sys.exit("Could not create sqlite DB: %s"%e)

  def add_plugin(self, plugin, color, size = 30):
    self.cur.execute("""INSERT INTO Plugins(Name, Color, Size)
                        Values(?, ?, ?);""", (plugin, color, size))
    self.db.commit()

  def get_plugins(self, plugin=None):
    where = ("Name = ?", plugin) if plugin else None
    return self._selectAllFrom("Plugins", where)

  def get_user(self, username):
    return self._selectAllFrom("Users", ("username = ?", username), 1)

  def teams_for_user(self, username):
    wh = """Team_ID IN(
              SELECT Team_ID FROM Users_In_Teams WHERE User_ID IN(
                SELECT User_ID FROM Users WHERE Username = ?))"""
    return self._selectAllFrom("Teams", (wh, username))

  def cases_for_team(self, team):
    wh = """Case_ID IN(
              SELECT Case_ID FROM Case_Access WHERE Team_ID IN(
                SELECT Team_ID FROM Teams WHERE Name = ?))"""
    return self._selectAllFrom("Cases", (wh, team))


  def _selectAllFrom(self, table, where=None, limit=None):
    vals = ()
    wh   = ""
    lim  = " LIMIT %s"%limit if limit else ""
    if where:
      if type(where) not in [tuple, list] or len(where) is not 2:
        raise(Exception)
      wh, vals = where
      wh="where "+" and ".join(wh) if type(wh) is list else "where %s"%wh
      vals = vals if type(vals) in [list, tuple] else (vals,)
    data=list(self.cur.execute("SELECT * FROM %s %s %s;"%(table, wh, lim), vals))
    dataArray=[]
    names = list(map(lambda x: x[0], self.cur.description))
    for d in data:
      j={}
      for i in range(0,len(names)):
        j[names[i].lower()]=d[i]
      dataArray.append(j)
    return dataArray
