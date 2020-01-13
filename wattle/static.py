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
    return render_template("home.html")

@static.route('/login')
def login():
    return render_template("login.html",url="login")

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
    f.close();
    json_string=json.dumps({'view':contents})
    return json_string


@static.route('/media/<path:path>')
def staticsend_media(path):
    return send_from_directory('static', path)    