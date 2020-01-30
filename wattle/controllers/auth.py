# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
#from .models import User
from .user import validate_user

auth = Blueprint('auth', __name__)

# On initial login This guy validates, then stores the valid user id in the session dict
@auth.route('/login', methods=['POST'])
def login():
    account = request.form.get('account')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user =validate_user(account,password)
    if user.is_authenticated==False:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    try:
        login_user(user, remember=remember)
        session['id']=user.id
        session['entity_id']=user.entity_id
        session['entity']=user.entity
        
    except Exception as ex:
        print("Auth Exception: {0}".format(ex))
    return redirect(url_for('static.home'))

# this guy logs a user out and removes the unique id from the session dict
@auth.route('/logout')
@login_required
def logout():
    session['id']=None
    logout_user()
    return redirect(url_for('static.unauth'))    