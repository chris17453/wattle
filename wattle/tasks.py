from . import db
from .groups import get_user_groups_by_account_id
from .entity import get_entity_id_by_name

from flask_wtf import FlaskForm 
from wtforms import BooleanField, StringField, PasswordField, \
     TextAreaField, IntegerField, SelectField, HiddenField, \
     DateTimeField, validators, FieldList, FormField
from wtforms.validators import InputRequired



def get_task_choices_by_account_id(id):
    query="select id,display from wattle.task"
    res=db.query(query);
    #print(res.data)
    choices=[]
    choices.append( (0,"None") )
    
    if res.data_length!=0:
        
        for task in res.data:
            choices.append( (task.id,task.display) )
    return choices


def get_tasks_by_account_id(account_id):
    query="select * from wattle.task where entity_id=@entity_id and group_id=@group_id"
    
    res=db.query(query,{'@entity_id':entity_id,'@group_id':group_id})
    
    if res.data_length!=0:
        return res.data
    return None


def get_task(entity_name,task_name):
    entity_id=get_entity_id_by_name(entity_name)
    
    query="select * from wattle.task where entity_id=@entity_id and name=@task_name LIMIT 1"
    
    res=db.query(query,{'@entity_id':entity_id,'@task_name':task_name})
    if res.data_length!=0:
        print (res.data[0].to_json())
        return res.data[0]

    #groups=get_user_groups_by_account_id(account_id)
    #print( groups)

    return None

def update_task():
    pass


# id,name,display,path,type,map,group_id,entity_id,created,modified,active
#1,jsoninput,Jsonify Input,tasks/jsonify/jsonify.py,py,0,1,1,,,1
class task_form(FlaskForm):
    id            =HiddenField  ('id'            ,render_kw={"placeholder": "ID"         ,"class":'form-control'})
    name          =StringField  ('Name'          ,render_kw={"placeholder": "Web Name"   ,"class":'form-control'})
    display       =StringField  ('Display'       ,render_kw={"placeholder": "Name"       ,"class":'form-control'})
    path          =StringField  ('Path'          ,render_kw={"placeholder": "Path"       ,"class":'form-control'})
    task_uid      =HiddenField  ('Task_UID'      ,render_kw={"placeholder": "Input Map"  ,"class":'form-control'})
    entity_id     =HiddenField  ('Entity_ID'     ,render_kw={"placeholder": "Entity ID"  ,"class":'form-control'})
    group_id      =HiddenField  ('Group_ID'      ,render_kw={"placeholder": "Group ID"   ,"class":'form-control'})
    created       =DateTimeField('Created'       ,render_kw={"placeholder": "Created"    ,"class":'form-control'})
    modified      =DateTimeField('Modified'      ,render_kw={"placeholder": "Modified"   ,"class":'form-control'})
    active        =BooleanField ('Active'        ,render_kw={"placeholder": "Active"     ,"class":'form-check-input'})
    sections=[
        {'anchor':'#Task','id':'Task','template':'task/task.html','display':'Task' },
        {'anchor':'#ConfigMap','id':'ConfigMap','template':'task/config_map.html','display':'Config Map' },
    ]
    
