from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import HiddenField
from wtforms import DateTimeField
from wtforms import validators
from wtforms import FieldList
from wtforms import FormField
from wtforms.validators import InputRequired


# label – The label of the field.
# validators – A sequence of validators to call when validate is called.
# filters – A sequence of filters which are run on input data by process.
# description – A description for the field, typically used for help text.
# id – An id to use for the field. A reasonable default is set by the form, and you shouldn’t need to set this manually.
# default – The default value to assign to the field, if no form or object input is provided. May be a callable.
# widget – If provided, overrides the widget used to render the field.
# render_kw (dict) – If provided, a dictionary which provides default keywords that will be given to the widget at render time.
# _form – The form holding this field. It is passed by the form itself during construction. You should never pass this value yourself.
# _name – The name of this field, passed by the enclosing form during its construction. You should never pass this value yourself.
# _prefix – The prefix to prepend to the form name of this field, passed by the enclosing form during construction.
# _translations – A translations object providing message translations. Usually passed by the enclosing form during construction. See I18n docs for information on message translations.

class template_form(FlaskForm):
    pass
class AutoForm:
    def __init__(self,form_schema,**kw_args):
        self.data=form_schema
        self.build()

    def build(self):
        form=template_form()
        for section in self.data:
            for field in section['fields']:
                element=None
                key=field['name']
                if   field['type']== 'Boolean':        element=BooleanField(       **self.valid_Boolean_args( field ) )
                elif field['type']== 'Decimal':        element=DecimalField(       **self.valid_Decimal_args( field ) )
                elif field['type']== 'Date':           element=DateField(          **self.valid_Date_args( field ) )
                elif field['type']== 'DateTime':       element=DateTimeField(      **self.valid_DateTime_args( field ) )
                elif field['type']== 'FieldList':      element=FieldList(          **self.valid_FieldList_args( field ) )
                elif field['type']== 'Float':          element=FloatField(         **self.valid_Float_args( field ) )
                elif field['type']== 'Form':           element=FormField(          **self.valid_Form_args( field ) )
                elif field['type']== 'Integer':        element=IntegerField(       **self.valid_Integer_args( field ) )
                elif field['type']== 'Radio':          element=RadioField(         **self.valid_Radio_args( field ) )
                elif field['type']== 'Select':         element=SelectField(        **self.valid_Select_args( field ) )
                elif field['type']== 'SelectMultiple': element=SelectMultipleField(**self.valid_SelectMultiple_args( field ) )
                elif field['type']== 'String':         element=StringField(        **self.valid_String_args( field ) )
                elif field['type']== 'Time':           element=TimeField(          **self.valid_Time_args( field ) )
                if element:
                    print(" Building element: "+key)
                    setattr(form,key,element)
                    #print(form)
        return form

    def append_field(self, form, name, field):
        setattr(form, name, field)
        return self

   
    def valid_Boolean_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Decimal_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Date_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_DateTime_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_FieldList_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Float_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Form_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Integer_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Radio_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Select_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_SelectMultiple_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_String_args(self,data):
        field=[]
        return self.valid_args(field,data)

    def valid_Time_args(self,data):
        field=[]
        return self.valid_args(field,data)
    
    def valid_string_args(data):
        field=[]
        return self.valid_args(field,data)

    def valid_args(self,field,data):
        base=['id','label','validators','filters','description','default','widget']
        args={}
        render_kw={}
        for key in data:
            # add base args... 
            if key in base:
                args[key]=data[key]
            # add field specific args
            elif key in field:
                args[key]=data[key]

            # else its a render keyword
            else:
                render_kw[key]=data[key]
            
        if len(render_kw)>0:
            args['render_kw']=render_kw
        
        return args

