from flask import Flask, request, send_from_directory, jsonify, render_template, session
from flask_cors import CORS
#from flask_login import LoginManager 
from .crud import tables, ddb_query_geany, initdb
from .user import get_user_by_id
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager 



def create_app():
    app = Flask(__name__, 
    static_folder = "./static",
    template_folder = "./static/views")
    CORS(app, resources={r'/*': {'origins': '*'}})


    app.config['SECRET_KEY'] = 'thefirstandlastthingithinkofisapasswordforyou'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            user=get_user_by_id(user_id)

        except Exception as ex:
            user=None
            pass
        
        return user

    @login_manager.request_loader
    def request_loader(request):
        return load_user(session['id'])

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for static elements of site
    from .static import static as static_blueprint
    app.register_blueprint(static_blueprint)

    return app





if __name__ == '__main__':
    app=create_app()
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080
    )
