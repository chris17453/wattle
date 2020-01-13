#from .crud import tables, ddb_query_geany, initdb
import ddb

db_config_dir="db"

# ddb autoloads SQL definitions in this directory once per flask init
db=ddb.engine(debug=None,config_dir=db_config_dir,mode='object')
#initdb(tables);
