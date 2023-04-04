from flask import request
from flask_security import login_required, current_user, login_user
from .models import User
from .playbooks import run_playbook
from .email import send_email
from flask import request, render_template
from flask import request, render_template, redirect, url_for
from flask import request
from app.playbooks import run_playbook
from app.email import send_email
from flask import render_template, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import UserModel
from app.email import send_email, send_email_to_triggers
from flask import request

# Login Resource - Handles the login page rendering and authentication
class LoginResource(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('welcome'))
        return make_response(render_template('login.html')) 

    def post(self):
        # Get email and password from the request
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Verify the user's password and log them in if successful
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('welcome'))
            #return {'message': f'Logged in as {current_user.email}'}
        else:
            return {'message': 'Invalid email or password'}, 401
        
# Registration Resource - Handles the registration page rendering and user registration
class RegistrationResource(Resource):
    def get(self):
        return make_response(render_template('register.html'))

    def post(self):
        # Get email and password from the request
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User already exists'}, 400

        # Create a new user (without any roles) and commit to the database
        user = user_datastore.create_user(email=email, password=password)
        user_datastore.commit()

        return {'message': 'User registered successfully. Awaiting admin approval.'}

# Welcome Resource - Handles the welcome page rendering and GET request execution
class WelcomeResource(Resource):
    @login_required
    def get(self):
        user_email = current_user.email
        user_roles = [role.name for role in current_user.roles]

        # Define the available GET endpoints for each role
        role_endpoints = {
            'Role1': ['/get1', '/get2'],
            'Role2': ['/get3', '/get4'],
            'Role3': ['/get5'],
            'Admin': ['/get1', '/get2', '/get3', '/get4', '/get5']
        }

        # Find the available GET endpoints for the current user
        get_endpoints = []
        for role in user_roles:
            get_endpoints.extend(role_endpoints.get(role, []))
        
        return make_response(render_template('welcome.html', user_email=user_email, get_endpoints=get_endpoints))
    
class BaseGetResource(Resource):
    role_required = None
    playbook_name = None

    @login_required
    def get(self):
        if self.role_required and not current_user.has_role(self.role_required):
            return {'message': 'Insufficient permissions'}, 403

        playbook_output = run_playbook(self.playbook_name)
        send_email("Playbook Output", playbook_output, current_user.email)

        return {'message': 'Playbook executed and output sent via email'}

class GetUser1(BaseGetResource):
    role_required = 'Role1'
    playbook_name = 'playbook1'

class GetUser2(BaseGetResource):
    role_required = 'Role2'
    playbook_name = 'playbook2'

# Add more GET resources as needed