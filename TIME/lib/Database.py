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


  def add_case(self, title, descr, notes, recurse):
    self.cur.execute("""INSERT INTO Cases(Title, Description, Notes, Recurse)
                        VALUES(%s, %s, %s, %s) RETURNING Case_ID;""",
                        (title, descr, notes, recurse))
    self.db.commit()
    return self.cur.fetchone()["case_id"]


  def create_new_snapshot(self, case_id, snapshot_time):
    self.cur.execute("""INSERT INTO Snapshots(Case_ID, Snapshot_time)
                        VALUES(%s, %s) RETURNING Snapshot_ID;""",
                        (case_id, snapshot_time))
    self.db.commit()
    return self.cur.fetchone()["snapshot_id"]


  def add_intel_type(self, intel_type):
    self.cur.execute("""WITH x as (
                          SELECT Intel_ID
                          FROM Intel_Types
                          Where Intel_Type = %s
                        ), y as (
                          INSERT INTO Intel_Types(Intel_Type)
                          SELECT %s
                          WHERE NOT EXISTS (SELECT 1 from x)
                          RETURNING Intel_ID)
                        SELECT Intel_ID  FROM x
                        UNION ALL
                        SELECT Intel_ID  FROM y""", (intel_type, intel_type))
    self.db.commit()
    return self.cur.fetchone()["intel_id"]


  def add_node(self, snapshot_id, uid, plugin, intel_id, name, label,
                     recurse_depth, size, color, x, y):
    self.cur.execute("""INSERT INTO Nodes(Snapshot_ID, UUID, Plugin, Type_ID,
                          Name, Label, Recurse_Depth, Size, Color, X, Y)
                        SELECT %s, %s, Plugin_ID, %s, %s, %s, %s, %s, %s, %s, %s
                          FROM Plugins
                          WHERE Name = %s;""",
                        (snapshot_id, uid, intel_id, name, label,
                         recurse_depth, size, color, x, y, plugin))
    self.db.commit()


  def add_edge(self, snapshot_id, source, target, label):
    self.cur.execute("""INSERT INTO Edges(Snapshot_ID, Source_ID, Target_ID, label
                        VALUES(%s, %s, %s, %s);""",
                        (snapshot_id, source, target, label))
    self.db.commit()


  def add_node_info(self, node_id, plugin, info):
    self.cur.execute("""INSERT INTO Node_Plugin_Info(Node_UUID, Plugin_ID, Info)
                        SELECT %s, Plugin_ID, %s
                          FROM Plugins
                          WHERE Name = %s;""",
                        (node_id, info, plugin))
    self.db.commit()


  def get_plugins(self, plugin=None):
    statement = "SELECT * FROM Plugins"
    if plugin: statement += " WHERE Name = %s"
    self.cur.execute(statement, (plugin,))
    return self.cur.fetchall()


  def get_teams(self):
    self.cur.execute("SELECT * FROM Teams")
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


  def get_case(self, case_number):
    self.cur.execute("""SELECT * FROM Cases WHERE Case_ID = %s;""", (case_number,))
    return self.cur.fetchall()


  def get_snapshots(self, case_number):
    self.cur.execute("""SELECT * FROM Snapshots WHERE Case_ID = %s;""", (case_number,))
    return self.cur.fetchall()


  def get_nodes_for_snapshot(self, snapshot_id):
    self.cur.execute("""SELECT * FROM Nodes WHERE Snapshot_ID = %s;""", (snapshot_id,))
    return self.cur.fetchall()


  def get_edges_for_snapshot(self, snapshot_id):
    self.cur.execute("""SELECT * FROM Edges WHERE Snapshot_ID = %s;""", (snapshot_id,))
    return self.cur.fetchall()


  def get_intel_types(self, intel_id = None):
    statement = "SELECT * FROM Intel_Types"
    if intel_id: statement += " WHERE Intel_ID = %s"
    self.cur.execute(statement, (intel_id,))
    return self.cur.fetchall()


# Backup database
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
      db_struct = db_struct.replace("SERIAL", "INTEGER")
      for s in db_struct.split(";"): self.cur.execute(s+";")
      if make_data:
        db_data   = open(os.path.join(lib, "db_data.sql")).read()
        for s in db_data.split(";"): self.cur.execute(s+";")
    except Exception as e:
      sys.exit("Could not create sqlite DB: %s"%e)


  def add_plugin(self, plugin, color, size = 30):
    self.cur.execute("""INSERT OR IGNORE INTO Plugins(Name, Color, Size)
                        Values(?, ?, ?);""", (plugin, color, size))
    self.db.commit()


  def add_case(self, title, descr, notes, recurse):
    self.cur.execute("""INSERT INTO Cases(Title, Description, Notes, Recurse)
                        VALUES(?, ?, ?, ?);""", (title, descr, notes, recurse))
    self.db.commit()
    return self.cur.lastrowid


  def create_new_snapshot(self, case_id, snapshot_time):
    self.cur.execute("""INSERT INTO Snapshots(Case_ID, Snapshot_time)
                        VALUES(?, ?);""", (case_id, snapshot_time))
    self.db.commit()
    return self.cur.lastrowid


  def add_intel_type(self, intel_type):
    self.cur.execute("""INSERT OR IGNORE INTO Intel_Types (Intel_Type)
                        VALUES(?)""", (intel_type,))
    self.db.commit()
    row = self._selectAllFrom("Intel_Types", ("Intel_Type = ?", intel_type), 1)
    return row[0]["intel_id"]


  def add_node(self, snapshot_id, uid, plugin, intel_id, name, label,
                     recurse_depth, size, color, x, y):
    self.cur.execute("""INSERT INTO Nodes(Snapshot_ID, UUID, Plugin, Type_ID,
                          Name, Label, Recurse_Depth, Size, Color, X, Y)
                        SELECT ?, ?, Plugin_ID, ?, ?, ?, ?, ?, ?, ?, ?
                          FROM Plugins
                          WHERE Name = ?;""",
                        (snapshot_id, uid, intel_id, name, label,
                         recurse_depth, size, color, x, y, plugin))
    self.db.commit()


  def add_edge(self, snapshot_id, source, target, label):
    self.cur.execute("""INSERT INTO Edges(Snapshot_ID, Source_ID, Target_ID, label
                        VALUES(?, ?, ?, ?);""", (snapshot_id, source, target, label))
    self.db.commit()


  def add_node_info(self, node_id, plugin, info):
    self.cur.execute("""INSERT INTO Node_Plugin_Info(Node_UUID, Plugin_ID, Info)
                        SELECT ?, Plugin_ID, ?
                          FROM Plugins
                          WHERE Name = ?;""", (node_id, info, plugin))
    self.db.commit()


  def get_plugins(self, plugin=None):
    where = ("Name = ?", plugin) if plugin else None
    return self._selectAllFrom("Plugins", where)


  def get_user(self, username):
    return self._selectAllFrom("Users", ("username = ?", username), 1)


  def get_teams(self):
    return self._selectAllFrom("Teams")


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


  def get_case(self, case_number):
    return self._selectAllFrom("Cases", ("Case_ID = ?", case_number), 1)


  def get_snapshots(self, case_number):
    return self._selectAllFrom("Snapshots", ("Case_ID = ?", case_number))


  def get_nodes_for_snapshot(self, snapshot_id):
    return self._selectAllFrom("Nodes", ("Snapshot_ID = ?", snapshot_id))


  def get_edges_for_snapshot(self, snapshot_id):
    return self._selectAllFrom("Edges", ("Snapshot_ID = ?", snapshot_id))


  def get_intel_types(self, intel_id = None):
    where = ("Intel_ID = ?", intel_id) if intel_id else None
    return self._selectAllFrom("Intel_Types", where)


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
