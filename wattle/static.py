from flask import Blueprint, render_template, redirect, url_for, request , send_from_directory, session
from flask_login import login_user, logout_user, login_required
#from .models import User
from . import db 

static = Blueprint('static', __name__,
    static_folder = "./static",
    template_folder = "./static/views")
    
@static.route('/')
def unauth():
    return render_template("unauth.html")

@static.route('/home')
@login_required
def home():
    menus=menu(session['id'])
    return render_template("home.html",title="Home",menus=menus,brand='Wattle')

@static.route('/login')
def login():
    login_title="Login"
    return render_template("login.html",url="login",title="Login",login_title=login_title)

@static.route('/bam/ipblocks/import')
def bam_IP4BLOCKS_import():
    blocks=[]
    return render_template("bam_IP4BLOCKS_import.html",blocks=blocks,title="IP4Blocks Import")


@static.route('/m/<entity>/<method>')
@login_required
def method_loader(entity,method):
    menus=menu(session['id'])
    return render_template("method.html",menus=menus)






def get_group_membership_by_id(account_id):
    res=db.query("select group_id from wattle.group_membership where account_id=@account_id",{'@account_id':account_id})
    # no gorups
    groups={}
    if res.data_length>0:
        for row in res.data:
            group_id=row['data']['group_id'].strip()
            groups[group_id]={'id':group_id,'type':'menu','name':group_id,'display':'UNK','links':[],'ordinal':0}  
        return groups

    return None

def get_groups_by_list(groups):
    # OK we have the groups... now pull the links
    if groups and len(groups)>0:
        group_where=[]
        parameters={}
        for group in groups:
            group_id=groups[group]['id']
            group_where.append('id=@group_id_{0}'.format(group_id))
            parameters['@group_id_{0}'.format(group_id)]=group_id

        where_clause="where "+" or ".join(group_where)
        res=db.query("select id,display,ordinal from wattle.group  {0} ".format(where_clause),parameters)
        if res.data_length>0:
            for row in res.data:
                group_id=row['data']['id']
                groups[group_id]['display']=row['data']['display']
                groups[group_id]['ordinal']=row['data']['ordinal']
            return groups
    return None

def get_methods_by_list(method_list):
    if method_list:
        methods={}
        methods_where=[]
        parameters={}
        for method in method_list:
            methods_where.append('id=@method_id_{0}'.format(method))
            parameters['@method_id_{0}'.format(method)]=method

        where_clause="where "+" or ".join(methods_where)
        res=db.query("select id,display,name,url from wattle.methods {0}".format(where_clause),parameters)
        if res.data_length!=0:
            for row in res.data:
                method_id=row['data']['id']
                display  =row['data']['display']
                name     =row['data']['name']
                url      =row['data']['url']
                if 'entity_display' in session:
                    entity_display=session['entity_display']
                else :
                    entity_display=''
                url=url.replace("{{ entity_display }}",str(entity_display))
                url="/m/"+url.replace("{{ method_display }}",display)
                methods[method_id]={'method_id':method_id,'display':display,'name':name,'url':url}
            return methods
    return None

def get_links_by_group_list(groups):
    # OK we have the groups... now pull the links
    group_membership_where=[]
    parameters={}
    if groups and len(groups)>0:
        for group in groups:
            group_id=groups[group]['id']
            group_membership_where.append('group_id=@group_id_{0}'.format(group_id))
            parameters['@group_id_{0}'.format(group_id)]=group_id

            where_clause="where "+" or ".join(group_membership_where)
            res=db.query("select id,display,method_id,group_id,ordinal from wattle.link {0} ".format(where_clause),parameters)
        
            if res.data_length>0:
                methods={}
                for row in res.data:
                    methods[row['data']['method_id']]=row['data']['method_id']
                methods=get_methods_by_list(methods)
                for row in res.data:
                    link_id     =row['data']['id']
                    group_id    =row['data']['group_id']
                    method_id   =row['data']['method_id']
                    link_display=row['data']['display']
                    ordinal     =row['data']['ordinal']
                    # maybe the method doesnt exist?
                    if methods==None or  method_id not in methods:
                        method_url  ="BOB"
                    else:
                        print( method_id)
                        method_url  =methods[method_id]['url']
                    groups[group_id]['links'].append({'type':'link','display':link_display,'id':link_id,'method_id':method_id,'group_id':group_id,'url':method_url,'ordinal':ordinal})

                return groups
    return None

def sort_groups(groups):
    # Sort the mess by menu ordinal, then link ordinal
    if groups:
        group2=[]
        for group in groups:
            group2.append(groups[group])

        group2=sorted(group2, key=lambda group: int(group['ordinal']))
        for group in group2:
            group['links']=sorted(group['links'],key=lambda link: int(link['ordinal']))

        return group2
    
    return None


def menu(account_id):
    groups=get_group_membership_by_id(account_id)
    groups=get_groups_by_list(groups)
    groups=get_links_by_group_list(groups)
    groups=sort_groups(groups)

    return groups

@static.route('/bam/ipblocks/list')
def bam_IP4BLOCKS():
    import importlib.util
    spec = importlib.util.spec_from_file_location("bam_api", "/home/cwatkin1/repos/chris17453/ipam-o-nator/src/bam_api.py")
    bam_api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bam_api)
    
    cred_file='/home/cwatkin1/repos/chris17453/ipam-o-nator/creds.json'

    bam=bam_api.bam_api(creds=cred_file)
    bam.login()    
    data=bam.get_et()

    blocks=[]
    for item in data:
        block={}
        block['id'] =item['id']
        block['name']=item['name']
        block['type']=item['type']
        tokens=item['properties'].split("|")
        #block['properties']=''
        for token in tokens:
            try:
                key,value =token.split('=')
                block[key]=value
            except:
                pass
                #if not token.strip().isspace():
                #    block['properties']+="|"+token.strip()
        blocks.append(block)

    return render_template("bam_IP4BLOCKS.html",blocks=blocks,title="IP4Blocks List")


@static.route('/js/<path:path>')
def send_js(path):
    #return path
    return send_from_directory('app/js/', path,mimetype="text/javascript")    

# all files are loaded as raw html, then encoded into json.
# templating then ocurs with variable expansion and returned 
# to the server
@static.route('/view/<path:path>')
def send_view(path):
    #return path
    f=open(path, "r")
    contents =f.read()
    f.close()
    json_string=json.dumps({'view':contents})
    return json_string


@static.route('/media/<path:path>')
def staticsend_media(path):
    return send_from_directory('static', path)    