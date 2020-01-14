from flask import Blueprint, render_template, redirect, url_for, request , send_from_directory
from flask_login import login_user, logout_user, login_required
#from .models import User

static = Blueprint('static', __name__,
    static_folder = "./static",
    template_folder = "./static/views")
    
@static.route('/')
def unauth():
    return render_template("unauth.html")

@static.route('/home')
@login_required
def home():
    return render_template("home.html",title="Home")

@static.route('/login')
def login():
    return render_template("login.html",url="login",title="Login")

@static.route('/bam/ipblocks/import')
def bam_IP4BLOCKS_import():
    blocks=[]
    return render_template("bam_IP4BLOCKS_import.html",blocks=blocks,title="IP4Blocks Import")


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