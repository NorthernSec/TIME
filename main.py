from TIME.lib.Case        import Case
from TIME.lib.CaseManager import CaseManager
from TIME.lib.Config      import Configuration as conf

intel_types={"ip":     conf.INTEL_IP,
             "domain": conf.INTEL_DOMAIN,
             "text":   conf.INTEL_TEXT}
case_manager = CaseManager()

case = Case()


def help():
  print("Commands:")
  print(" - new     - Open a new case (discards old)")
  print(" - add     - Add intel to the case")
  print("\tFormat: type=value")
  print("\t - ip")
  print("\t - domain")
  print(" - recurse - Set recursion depth (default 1)")
  print(" - nodes   - Print list of nodes")
  print(" - exit    - Exit the interface")
  print()

help()
while True:
  data = input("> ")
  if not data: continue
  data = data.split()
  command = data[0].lower()
  payload = data[1] if len(data) > 1 else None
  if   command == "new": case = Case()
  elif command == "add":
    try:
      key, intel = payload.split("=", 1)
      intel_type = intel_types[key]
    except:
      print("Please check the format"); help(); continue
    case_manager.add_intel(case, intel, intel_type)
  elif command == "exit": break
  elif command == "recurse":
    if payload:
      try:
        payload = int(payload)
      except:
        print("Please give an integer"); help(); continue
      case.recurse = payload
    else:
      print("Current recurse depth: %s"%str(case.recurse))
  elif command == "nodes":
    print("Node list:")
    for node in case.nodes:
      print(" - %s\t%s\t Distance: %s"%(node.name, node.label, node.recurse_depth))
