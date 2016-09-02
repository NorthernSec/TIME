#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Case Manager
#   Manages cases and the intelligence gathering for cases
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import queue
from uuid import uuid4

from TIME.lib.PluginManager import PluginManager
from TIME.lib.Case import Case, Edge, Node

class CaseManager():
  def __init__(self, plugin_manager = None):
    self.plug_man = plugin_manager
    if not plugin_manager:
      self.plug_man = PluginManager()
      self.plug_man.load_plugins()

  def add_intel(self, case, intel, intel_type):
    node = case.add_original_intel(intel, intel_type)
    if node:
      self.update_node_info(node)
      self.gather_intel(case, node)

  def update_node_info(self, node):
    info = self.plug_man.get_related_info(node.label, node.intel_type)
    for i in info:
      node.set_plugin_info(i[0], i[1])

  def gather_intel(self, case, node):
    work_queue = queue.Queue()
    work_queue.put(node)
    while not work_queue.empty():
      q_node = work_queue.get() # q_ for "query intel"
      # Look for next nodes
      n_intel = self.plug_man.get_related_intel(q_node.name, q_node.intel_type)
      for n in n_intel:
        # Turn the information into objects & add them to the case
        plugin, label, relation, intel_type, info = n
        node = Node(str(uuid4()), plugin, intel_type, label, relation,
                    q_node.recurse_depth + 1)
        if info: node.set_plugin_info(plugin, info)
        self.update_node_info(node)
        edge = Edge(q_node.uid, node.uid, relation)
        is_new = case.add_intel(node, edge)
        # If the recursion depth is not reached, continue
        if node.recurse_depth < case.recurse and is_new:
          work_queue.put(node)
