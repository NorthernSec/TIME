#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Plugin manager
#   Loads the plug-ins and handles the interaction with them
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import os
import importlib
import sys
import traceback

from TIME.lib.Config import Configuration as conf
import TIME.lib.DatabaseConnection as db
import TIME.lib.Toolkit as TK

class PluginManager():
  def __init__(self):
    self.plugins = {}

  def load_plugins(self):
    self.plugins = {}
    if not os.path.exists(conf.getPluginsettings()):
        print("[!] Could not find plugin loader file!")
        return
    # Read and parse plugin file
    data = open(conf.getPluginsettings(), "r").read()
    data = [x.split(maxsplit=3) for x in data.splitlines() if not x.startswith("#") and x]
    db.add_plugin_info(conf.NODE_ORIGINAL, "#666677")
    for x in [x for x in data if len(x) in [2, 3]]:
      try:
        x.extend(['']*(3-len(x))) # add empty args if none exist
        pluginName, loadstate, args = x
        if loadstate.lower() not in ["load", "enabled"]: # Skip if not load/enabled
          continue
        # Create object
        args = {y.split("=")[0]: y.split("=")[1] for y in args.split()}
        i = importlib.import_module("TIME.plugins.%s"%pluginName)
        plugin = getattr(i, pluginName.split("/")[-1])(**args)
        # Add to plugins
        self.plugins[pluginName] = plugin
        color = TK.generate_unique_color([x["color"] for x in self.get_all_plugins()])
        db.add_plugin_info(pluginName, color)
        print("[+] Plugin loaded: %s"%x[0])
      except Exception as e:
        print("[!] Failed to load plugin: %s: "%x[0])
        print("[!]  -> %s"%e)

  def get_related_intel(self, orig_intel, intel_type):
    intel = []
    for key in self.plugins.keys():
      try:
        new_intel = self.plugins[key].get_related_intel(orig_intel, intel_type)
        if new_intel:
          intel.extend([(key,)+x for x in new_intel])
      except Exception as e:
        print("[!] Failed to gather intel: %s: "%key)
        print("[!]  -> %s"%e)
        traceback.print_exc()
    # intel is a list of tuples of format (plugin, label, relation, intel type, info)
    return intel

  @classmethod
  def get_default_node_size(self, plugin):
    return db.get_plugins(plugin)["size"]

  @classmethod
  def get_default_node_color(self, plugin):
    return db.get_plugins(plugin)["color"]

  @classmethod
  def get_all_plugins(self):
    return db.get_plugins()
