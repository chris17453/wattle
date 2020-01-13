import ddb

CREATE_DB=None
db_config_dir="db"
db_name="wattle"

tables=[
{'file': '{0}/{1}/account.txt'   .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'account'     , 'columns':[ 'id', 'account'  , 'token'      , 'crud'   , 'entity_id', 'created'  , 'modified' , 'active'                                      ]},
{'file': '{0}/{1}/locations.txt' .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'location'    , 'columns':[ 'id', 'name'     , 'designation', 'address1' , 'address2' , 'city'     , 'postalcode'  , 'state'          ,'country'   ]},
{'file': '{0}/{1}/entity.txt'    .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'entity'      , 'columns':[ 'id', 'name'     , 'division'   , 'group'    , 'location' , 'parent_id'                                                ]},
{'file': '{0}/{1}/group.txt'     .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'group'       , 'columns':[ 'id', 'name'     , 'display'    , 'order'    , 'entity_id'                                                             ]},
{'file': '{0}/{1}/link.txt'      .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'link'        , 'columns':[ 'id', 'method_id', 'title'      , 'group_id'                                                                           ]},
{'file': '{0}/{1}/methods.txt'   .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'methods'     , 'columns':[ 'id', 'title'    , 'description', 'header'   , 'footer'   , 'theme'    , 'input_module', 'display_module', 'auto_run'  ]},
{'file': '{0}/{1}/methods.txt'   .format(db_config_dir,db_name), 'delimiter': ',', 'db':'{0}'.format(db_name),'table':'permissions' , 'columns':[ 'id', 'type'     , 'parent'     , 'child'    , 'deny'                                                                  ]},
]


class ddb_query_geany:
    def __init__(self,db=None,table=None,file=None,columns=None,delimiter=','):
        self.db       =db
        self.table    =table
        self.file     =file
        self.columns  =columns
        self.delimiter=delimiter

        if self.columns==None: RaiseException("Missing columns")
        if self.table  ==None: RaiseException("Missing table")
        if self.file   ==None: RaiseException("Missing file")
        

    # get table name
    def get_table(self):
        if self.db==None:
            return "'{0}'".format(self.table)
        else:
            return "'{0}'.'{1}' ".format(self.db,self.table)

    
    def get_where(self,where_tuples):
        if where_tuples==None:
            return ""
        for tuple in where_tuples:
            columns.append("`{0}`='{1}'".format(tuple,where_tuples[tuple]))
        
        where_data="WHERE "+" AND ".join(columns)
        return where_data
        

    # create a table
    def create_table(self,temp=None):
        if temp:
            return "CREATE TEMPORARY TABLE {0} ('{3}') file='{1}' delimiter='{2}'".format(self.get_table(),self.file,self.delimiter,"','".join(self.columns))
        return "CREATE TABLE {0} ('{3}') file='{1}' delimiter='{2}'".format(self.get_table(),self.file,self.delimiter,"','".join(self.columns))

    #  drop a table from the database
    def drop_table(self):
        return "DROP TABLE {0}".format(self.get_table())
    #    
    def truncate_table(self):
        return "TRUNCATE TABLE {0}".format(self.get_table())

    #    
    def select(self,columns,where_tuples=None):
        if columns==None:
            RaiseException("No data to select".format(self.get_table()))
        column_data=[]
        for column in columns:
            column_data.append("'{0}'".format(column))
        select_columns=','.join(column_data)
        return "SELECT {0} FROM {1} {2}".format(select_columns,self.get_table(),self.get_where(where_tuples))
    #    
    def update(self,data_tuples,where_tuples=None):
        if data_tuples==None:
            RaiseException("No data to update {0}".format(self.get_table()))

        columns=[]
        for column in data_tuples:
            columns.append("`{0}`='{1}'".format(column,data_tuples[column]))
        update_data=",".join(columns)
        return "UPDATE {0} SET {1} {2}".format(self.get_table(),update_data,self.get_where(where_tuples))
        
    #    
    def insert(self,data_tuples):
        columns=[]
        data=[]
        if data_tuples==None:
            RaiseException("No data to insert into {0}".format(self.get_table()))

        for column in self.columns:
            columns.append("'{0}'".format(column))
            if column in data_tuples:
                data.append("'{0}'".format(data_tuples[column]))
            else:
                data.append("")

        column_data=",".join(columns)
        value_data=",".join(data)
        

        for column in data_tuples:
            if column not in self.columns:
                raise Exception("Not a valid column for: {0}".format(self.get_table()))

        
        return "INSERT INTO TABLE {0} ({1}) VALUES ({2})".format(self.get_table(),column_data,value_data)

        
    #    
    def delete(self,where_tuples=None):
        return "DELETE FROM {0} {1})".format(self.get_table(),self.get_where(where_tuples))
        
    #    


def initdb(table_defs):
    if CREATE_DB==True:
        e=ddb.engine(debug=None,config_dir=db_config_dir)
    
    for table in table_defs:
        t=table
        crud=ddb_query_geany(t['db'],t['table'],t['file'],t['columns'],t['delimiter'])
        res=e.query(crud.create_table(temp=None))
        res.debug();
    return e

def test_crud():
    for table in tables:
        #print(table)

        crud=ddb_query_geany(table['db'],table['table'],table['file'],table['columns'],table['delimiter'])
        print ( crud.create_table() )
        print ( crud.truncate_table() )
        print ( crud.drop_table() )
        insert_data={}
        
        for column in table['columns']:
            insert_data[column]="@"+column
        print ( crud.insert(insert_data) )
        print ( crud.update(insert_data) )
        print ( crud.delete() )
        print ( crud.select(table['columns']) )
    



