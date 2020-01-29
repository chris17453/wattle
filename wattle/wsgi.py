from flask import Flask, request, send_from_directory, jsonify, render_template, session, abort
from flask_cors import CORS
#from flask_login import LoginManager 
from .crud import tables, ddb_query_geany, initdb
from .user import get_user_by_id
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager 
from .ddb import record
from .map import Map
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, record):
            # Implement code to convert Passport object to a dict
            return obj.to_json()
        else:
            JSONEncoder.default(self, obj)

#class CustomJSONDecoder(JSONDecoder):
#    def __init__(self, *args, **kwargs):
#        self.orig_obj_hook = kwargs.pop("object_hook", None)
#        super(CustomJSONDecoder, self).__init__(*args,
#            object_hook=self.custom_obj_hook, **kwargs)
#
#    def custom_obj_hook(self, dct):
#        # Calling custom decode function:
#        dct = HelperFunctions.jsonDecodeHandler(dct)
#        if (self.orig_obj_hook):  # Do we have another hook to call?
#            return self.orig_obj_hook(dct)  # Yes: then do it
#        return dct  # No: just return the decoded dict

def create_app():
    app = Flask(__name__, 
    static_folder = "./static",
    template_folder = "./static/views")
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.json_encoder = CustomJSONEncoder
    

    app.config['SECRET_KEY'] = 'thefirstandlastthingithinkofisapasswordforyou'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #from .models import User


    @login_manager.user_loader
    def load_user(user_id):
        if user_id==None:
            return None
        try:
            user=get_user_by_id(user_id)

        except Exception as ex:
            user=None
            pass
        
        return user

    @login_manager.request_loader
    def request_loader(request):
        if 'id' in session:
            user=load_user(session['id'])
            setup_session(user)
            return user

        return None

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for static elements of site
    from .static import static as static_blueprint
    app.register_blueprint(static_blueprint)
    
    def setup_session(user):
        # defaults
        account_id=None
        brand='Wattle'
        brand_short="W"
        entity=None
        menus=None
        # acount variables
        if user:
            entity=user.entity
            brand=entity.display
            account_id=user.id
            brand_short=entity.brand_short
            menus=menu(account_id,entity)
        
        session['menu']=menus
        session['brand']=brand
        session['brand_short']=brand_short
        session['account_id']=account_id
       
        #print(session)
    from .menu import menu
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error/404.html",state_vars=session),404

    return app





if __name__ == '__main__':
    app=create_app()
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080
    )
