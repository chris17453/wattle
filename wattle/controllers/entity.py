from . import db



# select the method id based on a url entry
def get_entity_id_by_name(entity_name):
    res=db.query("select id from wattle.entity where name=@entity_name LIMIT 1",{'@entity_name':entity_name})
    entity_id=None
    if res.data_length>0:
        return res.data[0].id
    return None