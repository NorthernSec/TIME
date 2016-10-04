#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database Abstraction Layer
#   Manage the databases (Postgres and sqlite), as well as the in-memory
#   database
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
from datetime     import datetime
from passlib.hash import pbkdf2_sha256

from TIME.lib.Database import PostgresDatabase, SQLITEDatabase
from TIME.lib.Case     import Case, Edge, Node

hash_rounds = 8000
salt_size   = 10

try:
  db = PostgresDatabase()
except:
  db = SQLITEDatabase()


def add_plugin(plugin, color, size = 30):
  try:
    db.add_plugin(plugin, color, size)
  except Exception as e:
    print(e)
    pass


def add_case(case):
  case.case_number = db.add_case(case.title, case.description, case.notes, case.recurse)
  snapshot_id      = create_new_snapshot(case)
  for node in case.nodes: add_node(snapshot_id, node)
  for edge in case.edges: add_edge(snapshot_id, edge)
  return case


def create_new_snapshot(case):
  return db.create_new_snapshot(case.case_number, datetime.now())


def add_intel_type(intel_type):
  return db.add_intel_type(intel_type)


def add_node(snapshot_id, node):
  intel_id = add_intel_type(node.intel_type)
  db.add_node(snapshot_id, node.uid, node.plugin, intel_id, node.name,
              node.label, node.recurse_depth, node.size, node.color, node.x, node.y)
  for plugin in node.info.keys():
    if node.info[plugin]: add_node_info(node, plugin, node.info[plugin])


def add_edge(snapshot_id, edge):
  db.add_edge(snapshot_id, edge.source, edge.target, edge.label)


def add_node_info(node, plugin, info):
  db.add_node_info(self, node.uid, plugin, info)


def get_plugins(plugin=None):
  data = db.get_plugins(plugin)
  if plugin: data = data[0] if len(data) is 1 else None
  return data if data else []


def user_exists(username):
  return True if get_user(username) else False


def get_user(username):
  data = db.get_user(username)
  return data[0] if data else None


def verify_user(username, password):
  user = get_user(username)
  return (user and pbkdf2_sha256.verify(password, user['hash']))


def get_teams():
  teams = db.get_teams()
  return teams if teams else []


def teams_for_user(username):
  teams = db.teams_for_user(username)
  return teams if teams else []


def get_cases_accessible_by_user(username):
  cases = []
  for team in teams_for_user(username):
    cases.extend([Case.from_dict(x) for x in db.cases_for_team(team['name'])])
  return cases


def get_case(case_number):
  data = db.get_case(case_number)
  return data[0] if data else None
