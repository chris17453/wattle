from . import db
from .tasks import get_task_choices_by_account_id
from .config_map import get_config_map
from flask_wtf import FlaskForm 
from wtforms import BooleanField, StringField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField, DateTimeField, validators, FieldList, FormField
from wtforms.validators import InputRequired

# select the method id based on a url entry
def get_entity_id_by_name(entity_name):
    res=db.query("select id from wattle.entity where name=@entity_name LIMIT 1",{'@entity_name':entity_name})
    entity_id=None
    if res.data_length>0:
        entity_id=res.data[0].id
    return entity_id


# select the method based on a url enttity/method
def get_method(entity_name,method_name):
    entity_id=get_entity_id_by_name(entity_name)
    method_dict={}
    
    if entity_id:
        res=db.query("select * from wattle.methods where name=@method_name and entity_id=@entity_id LIMIT 1",{'@method_name':method_name,'@entity_id':entity_id})
        if res.data_length>0:
            method=res.data
            for key in method:
                method_dict[key]=method[key]
    
    return method_dict


# select the method based on a url enttity/method
def update_method(form):
    query="""UPDATE wattle.methods 
    SET 
        name    = @name,
        display = @display,
        description = @description,
        url     = @url,
        output  = @output,
        task    = @task,
        input   = @input,
        template= @template,
        footer  = @footer,
        header  = @header,
        auto_run= @auto_run
    WHERE id=@id"""
    parameters={
                '@id'          :form.id.data,
                '@display'     :form.display.data,
                '@name'        :form.name.data,
                '@description' :form.description.data,
                '@url'         :form.url.data,
                '@output'      :form.output.data,
                '@task'        :form.task.data,
                '@input'       :form.input.data,
                '@template'    :form.template.data,
                '@footer'      :form.footer.data,
                '@header'      :form.header.data,
                '@auto_run'    :form.auto_run.data,
            }
    
    #for key in parameters:
    #    db.set_param(key,parameters[key])
    #sql=db.prepare_sql(query)
    #print(sql)

    res=db.query(query,parameters)
    res.debug()

    return res.success







class method_form(FlaskForm):

    display       = StringField  ('Display'       ,render_kw={"placeholder": "Web Name","class":'form-control'})
    name          = StringField  ('Name'          ,render_kw={"placeholder": "Name","class":'form-control'})
    description   = StringField  ('Description'   ,render_kw={"placeholder": "What does this Method do?","class":'form-control'})
    url           = StringField  ('URL'           ,render_kw={"placeholder": "The endpoint for this method","class":'form-control','readonly': True})
    id            = HiddenField  ('Method ID'     ,render_kw={"placeholder": "This method's ID","class":'form-control'})
    output        = SelectField  ('Display'       ,render_kw={"placeholder": "How the data is displayed","class":'form-control'},choices=[('','None'),('raw', 'Raw Output'), ('tablesorter', 'Tables'), ('json', 'json'),('xml', 'XML'),('yaml', 'YAML'),('zip', 'ZIP'),('targz', 'tar.gz')])
    task          = SelectField  ('Task'          ,render_kw={"placeholder": "How is the data processed","class":'form-control'},choices=get_task_choices_by_account_id(0))
    input         = FormField(get_config_map())
    template      = StringField  ('template'      ,render_kw={"placeholder": "A predefined UI snipit for displaying data","class":'form-control'})
    footer        = TextAreaField('Footer'        ,render_kw={"placeholder": "Post text","class":'form-control'})
    header        = TextAreaField('Header'        ,render_kw={"placeholder": "Pre text","class":'form-control'})
    auto_run      = BooleanField ('Auto Execute'  ,render_kw={"placeholder": "Run on page load?","class":'form-control'})
    yaml          = TextAreaField('Yaml'          ,render_kw={"placeholder": "Yaml representation of this method for inport or export.","class":'form-control'})
    



class component(FlaskForm):
    id            =HiddenField  ('id'            ,render_kw={"placeholder": "ID"         ,"class":'form-control'})
    name          =StringField  ('Name'          ,render_kw={"placeholder": "Web Name"   ,"class":'form-control'})
    display       =StringField  ('Display'       ,render_kw={"placeholder": "Name"       ,"class":'form-control'})
    path          =StringField  ('Path'          ,render_kw={"placeholder": "Path"       ,"class":'form-control'})
    map_id        =HiddenField  ('Map_ID'        ,render_kw={"placeholder": "Input Map"  ,"class":'form-control'})
    entity_id     =HiddenField  ('Entity_ID'     ,render_kw={"placeholder": "Entity ID"  ,"class":'form-control'})
    gropup_id     =HiddenField  ('Group_ID'      ,render_kw={"placeholder": "Group ID"   ,"class":'form-control'})
    created       =DateTimeField('Created'       ,render_kw={"placeholder": "Created"    ,"class":'form-control'})
    modified      =DateTimeField('Modified'      ,render_kw={"placeholder": "Modified"   ,"class":'form-control'})
    active        =BooleanField ('Active'        ,render_kw={"placeholder": "Active"     ,"class":'form-control'})