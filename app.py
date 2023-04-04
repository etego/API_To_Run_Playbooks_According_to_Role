from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Flask-Security
from .models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Flask-RESTful API
api = Api(app)

# Import and register the API resources
from .resources import (
    LoginResource, RegistrationResource, WelcomeResource, GetUser1, GetUser2,
    AdminApproveResource, AdminDeclineResource, AdminBanResource,
    AdminLogResource, AdminTokenResource, AdminPasswordResource
)

api.add_resource(LoginResource, '/login')
api.add_resource(RegistrationResource, '/register')
api.add_resource(WelcomeResource, '/welcome')
api.add_resource(GetUser1, '/get1')
api.add_resource(GetUser2, '/get2')
# Add more GET resources as needed
api.add_resource(AdminUserResource, '/admin/users')
api.add_resource(AdminApproveResource, '/admin/approve')
api.add_resource(AdminDeclineResource, '/admin/decline')
api.add_resource(AdminBanResource, '/admin/ban')
api.add_resource(AdminLogResource, '/admin/logs')
api.add_resource(AdminTokenResource, '/admin/tokens')
api.add_resource(AdminPasswordResource, '/admin/passwords')

if __name__ == '__main__':
    app.run(debug=True)
