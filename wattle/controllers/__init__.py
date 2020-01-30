#from .crud import tables, ddb_query_geany, initdb
from .ddb import engine

db_config_dir="wattle/db/conf"

# ddb autoloads SQL definitions in this directory once per flask init
db=engine(debug=None,config_dir=db_config_dir,mode='v2')
#res=db.query("show tables")
#res.debug()
#initdb(tables);


