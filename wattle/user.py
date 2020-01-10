import os
import jwt
import requests, json
from datetime import datetime, timedelta


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

def get_user_by_id(user_id):
    
    res=db.query("SELECT user from wattle.user where user_id=@user_id LIMIT 1",{'@user_id':user_id})
    print(res['data']);
    return res['data']