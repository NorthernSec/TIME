import sqlite3

path = ":memory:"
db=sqlite3.connect(path)

def ensureDB():
  db.execute('''CREATE TABLE IF NOT EXISTS Plugins
                (Plugin  Text     PRIMARY KEY,
                 Color   TEXT,
                 Size    INTEGER  DEFAULT 30);''')

##############
# Store data #
##############
# Plugins
def add_plugin_info(plugin, color, size = 30):
  db.execute("""INSERT OR REPLACE INTO Plugins(Plugin, Color, Size)
                VALUES(?, ?, ?)""", (plugin, color, size))
  db.commit()

##############
# Fetch data #
##############
# Plugins
def get_plugins(plugin=None):
  where = ["Plugin='%s'"%plugin] if plugin else []
  p = selectAllFrom("Plugins", where)
  if plugin:
    return p[0] if len(p) is 1 else None
  else: return p

def selectAllFrom(table, where=None):
  curs=db.cursor()
  wh="where "+" and ".join(where) if where else ""
  data=list(curs.execute("SELECT * FROM %s %s"%(table,wh)))
  dataArray=[]
  names = list(map(lambda x: x[0], curs.description))
  for d in data:
    j={}
    for i in range(0,len(names)):
      j[names[i].lower()]=d[i]
    dataArray.append(j)
  return dataArray
  
  
  
