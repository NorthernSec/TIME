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
import argparse
import os
import uuid
import sys
runPath = os.path.dirname(os.path.realpath(__file__))

from TIME.lib.Case        import Case
from TIME.lib.CaseManager import CaseManager
from TIME.lib.Config      import Configuration as conf
from TIME.lib.Visualizer  import Visualizer

intel_types={"ip":     conf.INTEL_IP,     "domain": conf.INTEL_DOMAIN,
             "text":   conf.INTEL_TEXT,   "email":  conf.INTEL_EMAIL,
             "asn":    conf.INTEL_ASN,    "md5":    conf.INTEL_MD5,
             "sha256": conf.INTEL_SHA256, "url":    conf.INTEL_URL,
             "user":   conf.INTEL_USER,   "phone":  conf.INTEL_PHONE}

case_manager = CaseManager()
case = Case()

def help():
  print("Commands:")
  print(" - new     - Open a new case (discards old)")
  print(" - add     - Add intel to the case")
  print("\tFormat: type=value")
  for key in sorted(intel_types.keys()):
    print("\t - %s"%key)
  print(" - recurse - Set recursion depth (default 1)")
  print(" - title   - Set title for case")
  print(" - descr   - Set description for case")
  print(" - notes   - Set notes for the case")
  print(" - nodes   - Print list of nodes")
  print(" - report  - Export a report in html format")
  print(" - exit    - Exit the interface")
  print()

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

def title(payload):
  if payload:
    case.title = payload
  else:
    print("Current title: %s"%case.title)

def description(payload):
  if payload:
    case.description = payload
  else:
    print("Current description: %s"%case.description)

def notes(payload):
  if payload:
    case.notes = payload
  else:
    print("Current notes: %s"%case.notes)

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

def interpretCommand(data):
  if not data: return True
  data = data.split(maxsplit=1)
  command = data[0].lower()
  payload = data[1] if len(data) > 1 else None
  if   command == "new":     case=Case()
  elif command == "add":     add(payload)
  elif command == "exit":    sys.exit()
  elif command == "recurse": recurse(payload)
  elif command == "title":   title(payload)
  elif command == "descr":   description(payload)
  elif command == "notes":   notes(payload)
  elif command == "nodes":   nodes()
  elif command == "report":  report()
  elif command == "help":    help()
  else: return False
  return True

if __name__ == '__main__':
  argParser = argparse.ArgumentParser(description='Admin account creator for the mongo database')
  argParser.add_argument('-f', type=str, help='File to parse')
  args = argParser.parse_args()

  if args.f:
    try:
      commands = open(args.f, "r").read().split("\n")
    except:
      sys.exit("Could not open %s. Does it exist?"%args.f)
    for command in commands:
      if command.startswith("#"): continue
      if not interpretCommand(command):
        print("Wrong command: %s"%command)
  else:
    print("Type 'help' for more info")
    while True:
      try:
        data = input("> ")
        if not interpretCommand(data):
          print("Unknown command. Press type help for help.")
      except (EOFError, KeyboardInterrupt):
        sys.exit()
