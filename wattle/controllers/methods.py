from . import db
from .entity import get_entity_id_by_name
from .tasks import get_task_choices_by_account_id
from .config_map import get_config_map_by_uid
from flask_wtf import FlaskForm 
from wtforms import BooleanField, StringField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField, DateTimeField, validators, FieldList, FormField
from wtforms.validators import InputRequired



# select the method based on a url enttity/method
def get_method(entity_name,method_name):
    entity_id=get_entity_id_by_name(entity_name)
    
    if entity_id:
        res=db.query("select * from wattle.methods where name=@method_name and entity_id=@entity_id LIMIT 1",{'@method_name':method_name,'@entity_id':entity_id})
        if res.data_length>0:
            return res.data[0]
    
    return None


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
    #print (self)
    template      = StringField  ('template'      ,render_kw={"placeholder": "A predefined UI snipit for displaying data","class":'form-control'})
    footer        = TextAreaField('Footer'        ,render_kw={"placeholder": "Post text","class":'form-control'})
    header        = TextAreaField('Header'        ,render_kw={"placeholder": "Pre text","class":'form-control'})
    auto_run      = BooleanField ('Auto Execute'  ,render_kw={"placeholder": "Run on page load?","class":'form-control'})
    yaml          = TextAreaField('Yaml'          ,render_kw={"placeholder": "Yaml representation of this method for inport or export.","class":'form-control'})
    sections=[
        {'anchor':'#Define','id':'Define','template':'method/define.html','display':'Define' },
        {'anchor':'#Style' ,'id':'Style' ,'template':'method/style.html' ,'display':'Style'  },
        {'anchor':'#Task'  ,'id':'Task'  ,'template':'method/task.html'  ,'display':'Task'   },
        {'anchor':'#Output','id':'Output','template':'method/output.html','display':'Output' } ]
    

