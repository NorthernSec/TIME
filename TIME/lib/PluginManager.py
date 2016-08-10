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

from TIME.lib.Config import Configuration as conf

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
        print("[+] Plugin loaded: %s"%x[0])
      except Exception as e:
        print("[!] Failed to load plugin: %s: "%x[0])
        print("[!]  -> %s"%e)

  def get_related_intel(self, orig_intel, intel_type):
    intel = []
    for key in self.plugins.keys():
      try:
        new_intel = self.plugins[key].get_related_intel(orig_intel, intel_type)
        intel.extend([(key,)+x for x in new_intel])
      except Exception as e:
        print("[!] Failed to gather intel: %s: "%key)
        print("[!]  -> %s"%e)
    # intel is a list of tuples of format (plugin, label, relation, intel type, info)
    return intel

  @classmethod
  def get_default_node_size(self, plugin):
    return 30

  @classmethod
  def get_default_node_color(self, plugin):
    return "#FFEE55"
