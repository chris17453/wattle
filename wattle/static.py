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
    #menus=[
    #{'type':'link','name':'Home'    ,'display':'Home'     ,'url':'#1','id':'menu_1'},
    #{'type':'menu','name':'Entity'  ,'display':'Entity'   ,'url':'#1','id':'menu_1','links': [{'name':'z','display':'y','url':'#8'},{'name':'z','display':'y','url':'#'},{'name':'z','display':'y','url':'#'}]},
    #{'type':'menu','name':'Group'   ,'display':'Group'    ,'url':'#2','id':'menu_2','links': [{'name':'z','display':'y','url':'#7'},{'name':'z','display':'y','url':'#'},{'name':'z','display':'y','url':'#'}]},
    #{'type':'menu','name':'Location','display':'Location' ,'url':'#3','id':'menu_3','links': [{'name':'z','display':'y','url':'#6'},{'name':'z','display':'y','url':'#'},{'name':'z','display':'y','url':'#'}]},
    #{'type':'menu','name':'Method'  ,'display':'Method'   ,'url':'#4','id':'menu_4','links': [{'name':'z','display':'y','url':'#5'},{'name':'z','display':'y','url':'#'},{'name':'z','display':'y','url':'#'}]},
    #]
    return render_template("home.html",title="Home",menus=menus,brand='Wattle')

@static.route('/login')
def login():
    return render_template("login.html",url="login",title="Login")

@static.route('/bam/ipblocks/import')
def bam_IP4BLOCKS_import():
    blocks=[]
    return render_template("bam_IP4BLOCKS_import.html",blocks=blocks,title="IP4Blocks Import")








def menu(account_id):
    permissions={}
    groups={}
    link={}
    parameters={}
    group_where=[]
    group_membership_where=[]

    # get groups for user
    res=db.query("select group_id from wattle.group_membership where account_id=@account_id",{'@account_id':account_id})
    # no gorups
    if res.data_length>0:
        for row in res.data:
            group_id=row['data']['group_id'].strip()
            groups[group_id]={'id':group_id,'type':'menu','name':group_id,'display':'UNK','links':[],'ordinal':0}  
            group_where.append('id=@group_id_{0}'.format(group_id))
            group_membership_where.append('group_id=@group_id_{0}'.format(group_id))
            parameters['@group_id_{0}'.format(group_id)]=group_id

        # OK we have the groups... now pull the links
        if len(groups)>0:
            where_clause="where "+" or ".join(group_where)
            res=db.query("select id,display,ordinal from wattle.group  {0} ".format(where_clause),parameters)
            if res.data_length>0:
                for row in res.data:
                    group_id_2=row['data']['id']
                    groups[group_id_2]['display']=row['data']['display']
                    groups[group_id_2]['ordinal']=row['data']['ordinal']
            

                where_clause="where "+" or ".join(group_membership_where)
                where_clause=""
                res=db.query("select id,display,method_id,group_id,ordinal from wattle.link {0} ".format(where_clause),parameters)
            
                if res.data_length>0:
                    for row in res.data:
                        link_id     =row['data']['id']
                        group_id    =row['data']['group_id']
                        method_id   =row['data']['method_id']
                        link_display=row['data']['display']
                        ordinal     =row['data']['ordinal']
                        groups[group_id]['links'].append({'type':'link','display':link_display,'id':link_id,'method_id':method_id,'group_id':group_id,'url':method_url,'ordinal':ordinal})

                    # Sort the mess by menu ordinal, then link ordinal
                    group2=[]
                    for group in groups:
                        group2.append(groups[group])

                    group3=sorted(group2, key=lambda group: int(group['ordinal']))
                    for group in group3:
                        group['links']=sorted(group['links'],key=lambda link: int(link['ordinal']))

                    return group3
                    
    return None

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