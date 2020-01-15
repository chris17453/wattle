

type row,column,group,text,numeric,file
name,type,text

class html:
    def __init__(self):
        pass

    def add(self,type,name,text):

    def render(self,elements):
        for element in elements:
            if   element['type']=='group':
                o+="<div>"+self.render(element['children'])+"</div>"
            elif element['type']=='text':
                o+='<input type="text" value="{1}" id="{0}" />'.format(element['uid'],element(value))
            elif element['type']=='numeric':
                o+='<input type="numeric" value="{1}" id="{0}" />'.format(element['uid'],element(value))
            elif element['type']=='date':
                o+='<input type="date" value="{1}" id="{0}" />'.format(element['uid'],element(value))
            elif element['type']=='datespan':
                o+='<input type="datespan" value="{1}" id="{0}" />'.format(element['uid'],element(value))
            elif element['type']=='key':
                o+='<input type="text" value="{1}" id="{0}" />'.format(element['uid'],element(value))
                o+='<input type="text" value="{1}" id="{0}" />'.format(element['uid'],element(value))
            else:
                o+="*"+self.render(element['children'])+"*"

            