from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask import redirect, url_for
from flask_security import logout_user

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Flask-RESTful API
api = Api(app)

# Configure the app with the database URI and security settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = 'email'

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)

# Import models and resources
from .models import User, Role
from .resources import LoginResource, RegistrationResource, BaseGetResource

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Register routes
from .routes import register_routes
register_routes(api)

# Import admin module
from . import admin

# Logot from the welcome page.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('loginresource'))