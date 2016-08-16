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
import os
import uuid
import sys
runPath = os.path.dirname(os.path.realpath(__file__))

from TIME.lib.Case        import Case
from TIME.lib.CaseManager import CaseManager
from TIME.lib.Config      import Configuration as conf
from TIME.lib.Visualizer  import Visualizer

intel_types={"ip":     conf.INTEL_IP,
             "domain": conf.INTEL_DOMAIN,
             "text":   conf.INTEL_TEXT}
case_manager = CaseManager()

def help():
  print("Commands:")
  print(" - new     - Open a new case (discards old)")
  print(" - add     - Add intel to the case")
  print("\tFormat: type=value")
  print("\t - ip")
  print("\t - domain")
  print(" - recurse - Set recursion depth (default 1)")
  print(" - title   - Set title for case")
  print(" - descr   - Set description for case")
  print(" - notes   - Set notes for the case")
  print(" - nodes   - Print list of nodes")
  print(" - report  - Export a report in html format")
  print(" - exit    - Exit the interface")
  print()

def new():
  return Case(title="", descr="", notes="", nodes=[], edges=[])

def add(payload):
  try:
    key, intel = payload.split("=", 1)
    intel_type = intel_types[key]
  except:
    print("Please check the format"); help(); return
  case_manager.add_intel(case, intel, intel_type)

def recurse(payload):
  if payload:
    try:
      payload = int(payload)
    except:
      print("Please give an integer"); help(); return
    case.recurse = payload
  else:
    print("Current recurse depth: %s"%str(case.recurse))

def nodes():
  print("Node list:")
  for node in case.nodes:
    print(" - %s\t%s\t Distance: %s"%(node.name, node.label, node.recurse_depth))

def report():
  v = Visualizer()
  report = v.generate_report(case)
  if not os.path.exists(os.path.join(runPath, "reports")):
    os.makedirs(os.path.join(runPath, "reports"))
  uid = str(uuid.uuid4())+".html"
  with open(os.path.join(runPath, "reports", uid), "w") as f:
    f.write(report)
  print("Report to ./reports/%s"%uid)

if __name__ == '__main__':
  help()
  case=new()
  while True:
    try:
      data = input("> ")
      if not data: continue
      data = data.split()
      command = data[0].lower()
      payload = data[1] if len(data) > 1 else None
      if   command == "new":     case=new()
      elif command == "add":     add(payload)
      elif command == "exit":    break
      elif command == "recurse": recurse(payload)
      elif command == "title":   case.title=payload
      elif command == "descr":   case.description=payload
      elif command == "notes":   case.notes=payload
      elif command == "nodes":   nodes()
      elif command == "report":  report()
      elif command == "help":    help()
      else:
        print("Unknown command. Press type help for help.")
    except (EOFError, KeyboardInterrupt):
      sys.exit()
