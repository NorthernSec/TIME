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
from passlib.hash import pbkdf2_sha256

from TIME.lib.Database import PostgresDatabase, SQLITEDatabase

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

def teams_for_user(username):
  teams = db.teams_for_user(username)
  return teams if teams else []

def get_cases_accessible_by_user(username):
  cases = []
  for team in teams_for_user(username):
    cases.extend(db.cases_for_team(team['name']))
  for case in cases: CaseManager.case_from_dict(case)
  return cases
    



