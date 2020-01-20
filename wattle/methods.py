from . import db
from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, IntegerField, validators


# select the method id based on a url entry
def get_entity_id_by_name(entity_name):
    res=db.query("select id from wattle.entity where name=@entity_name LIMIT 1",{'@entity_name':entity_name})
    entity_id=None
    if res.data_length>0:
        entity_id=res.data[0]['data']['id']
    return entity_id


# select the method based on a url enttity/method
def get_method(entity_name,method_name):
    entity_id=get_entity_id_by_name(entity_name)
    method=None
    
    if entity_id:
        res=db.query("select * from wattle.methods where name=@method_name and entity_id=@entity_id LIMIT 1",{'@method_name':method_name,'@entity_id':entity_id})
        if res.data_length>0:
            method=res.data[0]['data']
    return method




class method_form(Form):
    method_id     = IntegerField ('method_id',     )
    description   = StringField  ('description',   )
    display       = StringField  ('display',       )
    display_module= StringField  ('display_module',)
    footer        = TextAreaField('footer',        )
    header        = TextAreaField('header',        )
    input_module  = StringField  ('input_module',  )
    name          = StringField  ('name',          )
    theme         = StringField  ('theme',         )
    url           = StringField  ('url',           )
    auto_run      = BooleanField ('auto_run',      )
