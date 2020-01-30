import os
import jwt
import requests, json
from datetime import datetime, timedelta

from . import db

def validate_user(account,password,entity):
    return {'id':1}

# [SECURITY]********************************************************************

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20


#@app.before_request
def auth_gatekeeper():
    request.user = None
    jwt_token = request.headers.get('authorization', None)
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET,algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return json_response({'message': 'Token is invalid'}, status=400)

        request.user = payload['user_id']

def json_response(body='', **kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    return web.Response(**kwargs)

# this grants you your token. It's important because everything uses a token
#@app.route('/v1/login/<entity>')
def login(entity):
    post_data = request.post()

    try:
        user =validate_user(post_data['account'],post_data['password'],entity)
    except:
        return json_response({'message': 'BAD'}, status=400)

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return json_response({'token': jwt_token.decode('utf-8')})


# [API]*************************************************************************


#@app.route('/api/')
def api():
    return app.send_static_file('pages/home.html')


    
 
#def get_entity_by_name(name=None):
#
#    if name==None:
#        raise Exception("No name provided")
#
#    e.set_parameter("@name",name)
#    query="SELECT FROM wattle.entity WHERE name=@name LIMIT 1"
#    res=e.execute(query)
#    success==True:
#
#
#def get_user_by_name(name=None):
#    if name==None:
#        raise Exception("No name provided")
#
#    query="SELECT FROM wattle.user WHERE name=@name LIMIT 1"
#    e.set_parameter("@name",name)
#    e.execute(query)
#




class user:
    id=None
    account=None
    token=None

    is_authenticated=False
    is_active=False
    is_anonymous=True
    entity_id=0

    id="UNK"
    def __init__(self):
        pass

    def login(self,account,token):
        try:
            res=db.query("SELECT id,account,token,entity_id,active from wattle.account where account=@account and token=@token  LIMIT 1",{'@account':account,'@token':token})
            #res.debug()
            if res.data_length==0:
                return None
            data=res.data[0]
            
            self.id       =data.id
            self.account  =data.account
            self.token    =data.token
            self.entity_id=data.entity_id
            self.logged_in=True

            try:
                if data.active=='1':
                    self.is_active=True
            except Exception as ex:
                print("111Rrrr: ",ex,data.to_json())
                pass


            self.load_entity()
            self.is_authenticated=True
            try:
                if data.active=='1':
                    self.is_active=True
            except Exception as ex:
                print("222LERRrrr: ",ex,data.to_json())


            self.is_anonymous=False

        except Exception as ex:
            print("Login Err: "+str(ex) )
            pass

    def load_by_id(self,id):
        res=db.query("SELECT account,token,entity_id from wattle.account where id=@account_id LIMIT 1",{'@account_id':id})
        data=res.data[0]
        account=data.account
        token=data.token
        self.entity_id=data.entity_id
        self.load_entity()
        self.login(account,token)
    
    def load_entity(self):
        res=db.query("SELECT * from wattle.entity where id=@entity_id LIMIT 1",{'@entity_id':self.entity_id})
        
        if res.data_length>0:
            data=res.data[0]
            self.entity=data
        else:
            self.entity={}

    
    def get_id(self):
        if self.logged_in:
            return self.id
        return None


def validate_user(account,token):
    try:
        user_session=user()
        user_session.login(account,token)
    except Exception as ex:
        #print(ex)
        pass
    return user_session

def get_user_by_id(account_id):
    user_session=user()
    user_session.load_by_id(account_id)
    return user_session


