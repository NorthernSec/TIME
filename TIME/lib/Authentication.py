#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Plugin manager
#
# Software is free software released under the "Modified BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
import os
import importlib

import TIME.lib.DatabaseLayer as db
from TIME.lib.Config import Configuration as conf

# Constants
UNREACHABLE   = -1
WRONG_CREDS   =  0
AUTHENTICATED =  1

class AuthenticationMethod:
  # Force users to override this
  def validateUser(self, user, pwd):
    return WRONG_CREDS

class AuthenticationHandler:
  def __init__(self):
    self.methods = []
    self._load_methods()

  def _load_methods(self):
    self.methods = []
    if not os.path.exists(conf.getAuthLoadSettings()):
        print("[!] Could not find auth loader file!")
        return
    # Read and parse plugin file
    data = open(conf.getAuthLoadSettings(), "r").read()
    data = [x.split(maxsplit=2) for x in data.splitlines() if not x.startswith("#") and x]
    for x in [x for x in data if len(x) in [2, 3]]:
      try:
        x.extend(['']*(3-len(x))) # add empty args if none exist
        method, authType, args = x
        if authType.lower() not in ["required", "sufficient"]: # Skip if authType not known
          continue
        # Create object
        args = {y.split("=")[0]: y.split("=")[1] for y in args.split()}
        i = importlib.import_module("lib.authenticationMethods.%s"%method)
        authMethod = getattr(i, method.split("/")[-1])(**args)
        # Add object to list
        self.methods.append((method, authType.lower(), authMethod))
        print("[+] Loaded Auth Method %s"%x[0])
      except Exception as e:
        print("[!] Failed to load Auth Method %s: "%x[0])
        print("[!]  -> %s"%e)

  def isValidUser(self, user):
    return db.user_exists(user)

  def validateUser(self, user, password):
    user_obj = db.get_user(user)
    if not user_obj: return False
    # 'local_only' users bypass other auth methods. If the user is not, 
    #  we try the other auth methods first
    if (not "local_only" in user_obj.keys()
       or user_obj["local_only"] is False):
      for name, authType, method in self.methods:
        try:
          result = method.validateUser(user, password)
          if result is UNREACHABLE:   continue     # Skip to next
          if result is AUTHENTICATED: return True  # Successful
          if (authType == "required"   and result is WRONG_CREDS): return False
          if (authType == "sufficient" and result is WRONG_CREDS): continue
        except Exception as e:
          print("[!] Exception trying to authenticate user: %s: "%name)
          print("[!]  -> %s"%e)
    # If we reach here, all methods (if any) failed to authenticate the user
    #  so we check the user against the local database.
    return db.verify_user(user, password)

