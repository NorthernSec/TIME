import queue
from TIME.lib.PluginManager import PluginManager
from TIME.lib.Case import Case, Edge, Node

class CaseManager():
  def __init__(self):
    self.plug_man = PluginManager()
    self.plug_man.load_plugins()

  def add_intel(self, case, intel, intel_type):
    if case.add_original_intel(intel, intel_type):
      node = Node(intel, "Original", intel_type, "Original", intel, 0)
      self.gather_intel(case, node)

  def gather_intel(self, case, node):
    work_queue = queue.Queue()
    work_queue.put(node)
    while not work_queue.empty():
      q_node = work_queue.get() # q_ for "query intel"
      n_intel = self.plug_man.get_related_intel(q_node.uid, q_node.intel_type)
      for n in n_intel:
        # Turn the information into objects & add them to the case
        plugin, label, relation, intel_type, info = n
        node = Node(label, plugin, intel_type, relation, label,
                    q_node.recurse_depth + 1, info=info)
        edge = Edge(q_node.uid, node.uid, relation)
        case.add_intel(node, edge)
        # If the recursion depth is not reached, continue
        if node.recurse_depth < case.recurse:
          work_queue.put(node)
    
    
    
    
    # Load case and manage the threat intel gathering, like in Ostrica.py.
    # CaseManager should be called by a flask function, so think about how
    #  to implement it. 
    

