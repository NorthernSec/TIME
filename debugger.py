#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Interface
#   Interface for the tool. Very minimalistic, but has all the main 
#   functionalities
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import sys
import json
from bson import json_util

from main import *

from TIME.lib.Toolkit import *

def debug(obj):
  text = json.dumps(to_dict(obj), indent=2, default=json_util.default)
  open("TIME_debug.log", "a").write(text)

if __name__ == '__main__':
  print("Type 'help' for more info")
  while True:
    try:
      data = input("> ")
      if data.startswith("."):
        data = "exec " + data[1:]
      if data.lower().startswith("exec "):
        data = data.split(maxsplit=1)
        payload = data[1] if len(data) > 1 else None
        if payload:
          try:
            exec(payload)
          except Exception as e:
            print(e)
      else:
        if not interpretCommand(data):
          print("Unknown command. Press type help for help.")
    except (EOFError, KeyboardInterrupt):
      sys.exit()
