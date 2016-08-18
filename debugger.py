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

from main import *

if __name__ == '__main__':
  print("Type 'help' for more info")
  while True:
    try:
      data = input("> ")
      if data.lower().startswith("exec "):
        data = data.split(maxsplit=1)
        payload = data[1] if len(data) > 1 else None
        if payload:
          exec(payload)
      else:
        if not interpretCommand(data):
          print("Unknown command. Press type help for help.")
    except (EOFError, KeyboardInterrupt):
      sys.exit()
