from . import db
from flask_wtf import Form 
from wtforms import BooleanField, StringField, PasswordField, TextAreaField, IntegerField, validators
from wtforms.validators import InputRequired

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
    display       = StringField  ('Display'       ,render_kw={"placeholder": "Web Name","class":'form-control'})
    name          = StringField  ('Name'          ,render_kw={"placeholder": "Name","class":'form-control'})
    description   = StringField  ('Description'   ,render_kw={"placeholder": "What does this Method do?","class":'form-control'})
    url           = StringField  ('URL'           ,render_kw={"placeholder": "The endpoint for this method","class":'form-control'})
    method_id     = IntegerField ('Method ID'     ,render_kw={"placeholder": "This method's ID","class":'form-control'})

    display_module= StringField  ('Display Module',render_kw={"placeholder": "How the data is displayed","class":'form-control'})
    input_module  = StringField  ('Engine Module' ,render_kw={"placeholder": "How is the data processed","class":'form-control'})
    input_module  = StringField  ('Input Module'  ,render_kw={"placeholder": "How is the data collected","class":'form-control'})
    theme         = StringField  ('Theme'         ,render_kw={"placeholder": "Style","class":'form-control'})
    footer        = TextAreaField('Footer'        ,render_kw={"placeholder": "Post text","class":'form-control'})
    header        = TextAreaField('Header'        ,render_kw={"placeholder": "Pre text","class":'form-control'})
    auto_run      = BooleanField ('Auto Execute'  ,render_kw={"placeholder": "Run on page load?","class":'form-control'})
