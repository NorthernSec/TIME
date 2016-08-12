
from datetime import datetime
from uuid import uuid4

from TIME.lib.PluginManager import PluginManager as pm

class Case():
  def __init__(self, case_nr=None, title=None, descr=None, notes=None,
                     created=None, recurse=1, nodes=[], edges=[]):
    self.case_number = case_nr
    self.title       = title
    self.description = descr
    self.notes       = notes
    self.recurse     = recurse
    self.nodes       = nodes
    self.edges       = edges

  def original_intel(self):
    return [n for n in self.nodes if n.recurse_depth is 0]

  def clean_gathered_intel(self):
    self.nodes, self.edges = self.original_nodes(), []

  def clean_all_intel(self):
    self.nodes, self.edges = [], []

  def add_original_intel(self, intel, intel_type):
    if not any(n.uid==intel and n.plugin=="Original" and
               n.intel_type==intel_type for n in self.nodes):
      self.nodes.append(Node(str(uuid4()), "Original", intel_type, "Original", intel, 0))
      return True
    return False

  def add_intel(self, node, edge):
    if not any(n.label==node.label and n.intel_type==node.intel_type and
               n.info ==node.info  for n in self.nodes):
      self.nodes.append(node)
    else:
      matching = next((n for n in self.nodes if n.label==node.label and
                                                n.intel_type==node.intel_type and
                                                n.info==node.info), None)
      edge.target = matching.uid
    if not any(e.target==edge.target and e.source==edge.source and
               e.label ==edge.label for e in self.edges):
      self.edges.append(edge)


class Node():
  def __init__(self, uid, plugin, intel_type, name, label, depth,
                     size=None, color=None, info=None, dateFound=None):
    self.uid           = uid
    self.plugin        = plugin
    self.intel_type    = intel_type
    self.name          = name
    self.label         = label
    self.recurse_depth = depth
    self.size    = size  if size  else pm.get_default_node_size(plugin)
    self.color   = color if color else pm.get_default_node_color(plugin)
    self.info          = info
    self.dateFound     = dateFound if dateFound else datetime.now()

class Edge():
  def __init__(self, source_id, target_id, label):
    self.source = source_id
    self.target = target_id
    self.label  = label
