#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Case, Node, Edge
#   Encompasses the main objects for the relations:
#    - Case: A threat intel case, with documentation, nodes and edges
#    - Node: A piece of intel
#    - Edge: A relationship between two nodes
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import copy
from datetime import datetime
from uuid import uuid4

from TIME.lib.Config import Configuration as conf

class Case():
  def __init__(self, case_nr=None, title=None, descr=None, notes=None,
                     recurse=1, nodes=None, edges=None):
    self.case_number = case_nr
    self.title       = title
    self.description = descr
    self.notes       = notes
    self.recurse     = recurse
    self.nodes       = nodes if nodes else []
    self.edges       = edges if edges else []

  def original_intel(self):
    return [n for n in self.nodes if n.recurse_depth is 0]

  def clean_gathered_intel(self):
    self.nodes, self.edges = self.original_nodes(), []

  def clean_all_intel(self):
    self.nodes, self.edges = [], []

  def add_original_intel(self, intel, intel_type):
    if not any(n.uid==intel and n.plugin==conf.NODE_ORIGINAL and
               n.intel_type==intel_type for n in self.nodes):
      node = Node(str(uuid4()), conf.NODE_ORIGINAL, intel_type, conf.NODE_ORIGINAL, intel, 0)
      self.nodes.append(node)
      return node
    return None

  def add_intel(self, node, edge):
    if not any(n.label==node.label and n.intel_type==node.intel_type and
               n.info ==node.info  for n in self.nodes):
      self.nodes.append(node)
    else:
      matching = next((n for n in self.nodes if n.label==node.label and
                                                n.intel_type==node.intel_type and
                                                n.info==node.info), None)
      edge.target = matching.uid
    if not any(e.target==edge.target and e.source==edge.source for e in self.edges):
      if not any(e.target==edge.source and e.source==edge.target for e in self.edges):
        self.edges.append(edge)
    return False if "matching" in vars() else True

  @classmethod
  def from_dict(self_class, d):
    try:
      nodes = list(filter(None, [Node.from_dict(node) for node in d.get('nodes', [])]))
      edges = list(filter(None, [Edge.from_dict(node) for node in d.get('edges', [])]))
      return self_class(d['case_id'], d['title'], d['description'], d['notes'], d['recurse'], nodes, edges)
    except:
      None

class Node():
  def __init__(self, uid, plugin, intel_type, name, label, depth,
                     size=None, color=None, info=None, x=None, y=None):
    # Importing here, to avoid circular importing
    from TIME.lib.PluginManager import PluginManager as pm

    self.uid           = uid
    self.plugin        = plugin
    self.intel_type    = intel_type
    self.name          = name
    self.label         = label
    self.recurse_depth = depth
    self.size    = size  if size  else pm.get_default_node_size(plugin)
    self.color   = color if color else pm.get_default_node_color(plugin)
    self.info          = copy.deepcopy(info) if info else {}
    self.x             = x
    self.y             = y

  def set_plugin_info(self, plugin, info):
    self.info[plugin] = info

  @classmethod
  def from_dict(self_class, d):
    try:
      return self_class(d['uuid'], d['plugin'], d['type'], d['name'],
                        d['label'], d['recurse_depth'], d['size'],
                        d['color'], d['x'], d['y'])
    except:
      return None

class Edge():
  def __init__(self, source_id, target_id, label):
    self.source = source_id
    self.target = target_id
    self.label  = label

  @classmethod
  def from_dict(self, d):
    try:
      return Edge(d['source_id'], d['target_id'], d['label'])
    except:
      return None
