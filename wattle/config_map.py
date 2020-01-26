from . import db
from .tasks import get_task_choices_by_account_id

from flask_wtf import FlaskForm 
from wtforms import BooleanField, StringField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField, DateTimeField, validators, FieldList
from wtforms.validators import InputRequired




def get_config_map_by_uid(uid):
    res=db.query("SELECT * FROM wattle.config_map where uid=@uid",{'@uid':uid})
    if res.data_length==0:
        return None

# base object for the form
class config_map_form(FlaskForm):
    pass

# generates the form on the fly        
class config_map_helper():
    
    def __init__(self):
        self.config_map=config_map_form

        self.add_field("txtarea","b1")
        self.add_field("str"    ,"b2")
        self.add_field("hidden" ,"b3")
        self.add_field("select" ,"b4")
        self.add_field("bool"   ,"b5")
        pass
        
    def add_field(self,field_type,field_id,place_holder='Enter a Value',choices=[]):
        field=None
        if field_type=='txtarea':
            field=TextAreaField(field_id  ,render_kw={"placeholder": place_holder, "class": 'form-control'})
        elif field_type=='str':
            field=StringField  (field_id  ,render_kw={"placeholder": place_holder, "class": 'form-control'})
        elif field_type=='hidden':
            field=HiddenField  (field_id  ,render_kw={"placeholder": place_holder, "class": 'form-control'})
        elif field_type=='select':
            field=SelectField  (field_id  ,render_kw={"placeholder": place_holder, "class":'form-control'},choices=choices)
        elif field_type=='bool':
            field=BooleanField ('Auto Execute'  ,render_kw={"placeholder": place_holder, "class": 'form-control'})
        else:
            return None
        try:
            setattr(self.config_map, field_id,field)
        except Exception as ex:
            pass
        return True


# this is what returns the dynamic form
def get_config_map():
    helper=config_map_helper()
    helper.add_field("txtarea","b1")
    helper.add_field("str"    ,"b2")
    helper.add_field("hidden" ,"b3")
    helper.add_field("select" ,"b4")
    helper.add_field("bool"   ,"b5")
    return helper.config_map