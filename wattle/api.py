from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request , send_from_directory, session, abort, flash
from flask_login import login_user, logout_user, login_required
#from .models import User
from .controllers.methods import get_method, method_form, update_method
from .controllers.tasks import get_task, task_form, update_task
from .controllers.user import validate_user

from pprint import pprint

api = Blueprint('api', __name__,
    static_folder = "./static",
    template_folder = "./views")
    
@api.route('/')
def unauth():
    #session['brand']="Wattle"
    #session['brand_short']="W"
    return render_template("not-logged-in/unauth.html",state_vars=session)

@api.route('/home')
@login_required
def home():
    return render_template("home/home.html",title="Home",state_vars=session)



@api.route('/m/<entity>/<method>',methods=['GET', 'POST'])
@login_required
def method_loader(entity,method):
    method=get_method(entity,method)
    if method==None:
        abort(404)

    

    #'name','display','description','url','header','footer','theme','input_module','display_module','auto_run'
    #pprint (method)
    return render_template("method/method.html",state_vars=session)


@api.route('/m/c/<entity>/<method>',methods=['GET', 'POST'])
@login_required
def method_config(entity,method):
    # on initital Load, Pull from database
    if request.method == 'GET':
        method=get_method(entity,method)
        if method==None:
            abort(404)

        form = method_form(**method).build()
    else:
        form = method_form(obj=request.form).build()

    #and form.validate()
    if request.method == 'POST' :
        flash("Submitted")
        update_method(form)

    #'name','display','description','url','header','footer','theme','input_module','display_module','auto_run'
    #pprint (method)
    print(session)
    return render_template("method/configure.html",state_vars=session,form=form)


@api.route('/t/c/<entity>/<task>',methods=['GET', 'POST'])
@login_required
def task_config(entity,task):
    # on initital Load, Pull from database
    if request.method == 'GET':
        task=get_task(entity,task)
        if task==None:
            abort(404)
        
        form = task_form(**task)
    else:
        form = task_form(obj=request.form)

    #and form.validate()
    if request.method == 'POST' :
        flash("Submitted")
        update_task(form)

    print(session['entity'])
    return render_template("task/configure.html",state_vars=session,form=form)






@api.route('/bam/ipblocks/list')
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

    return render_template("bam_IP4BLOCKS.html",blocks=blocks,title="IP4Blocks List",state_vars=session)


@api.route('/js/<path:path>')
def send_js(path):
    #return path
    return send_from_directory('app/js/', path,mimetype="text/javascript")    

# all files are loaded as raw html, then encoded into json.
# templating then ocurs with variable expansion and returned 
# to the server
@api.route('/view/<path:path>')
def send_view(path):
    #return path
    f=open(path, "r")
    contents =f.read()
    f.close()
    json_string=json.dumps({'view':contents})
    return json_string


@api.route('/media/<path:path>')
def apisend_media(path):
    return send_from_directory('static', path)    



# On initial login This guy validates, then stores the valid user id in the session dict
@api.route('/login', methods=['POST','GET'])
def login():
    if request.method=='GET':
        login_title="Login"
        return render_template("auth/login.html",url="login",title="Login",login_title=login_title,state_vars=session)
    elif request.method=='POST':
        account = request.form.get('account')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user =validate_user(account,password)

        if user.is_authenticated==False:
            flash('Please check your login details and try again.')
            return redirect(url_for('api.login')) # if user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        try:
            login_user(user, remember=remember)
            session['id']=user.id
            session['entity_id']=user.entity_id
            session['entity']=user.entity
        
        except Exception as ex:
            print("Auth Exception: {0}".format(ex))
        return redirect(url_for('api.home'))

# this guy logs a user out and removes the unique id from the session dict
@api.route('/logout')
@login_required
def logout():
    session['id']=None
    logout_user()
    return redirect(url_for('api.unauth'))        