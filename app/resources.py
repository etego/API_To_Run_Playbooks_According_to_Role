from flask import request, render_template, redirect, url_for
from flask_restful import Resource
from flask_security import login_required, current_user, login_user
from .models import User
from .email import send_email
from flask import request, render_template, redirect, url_for
from .playbooks import run_playbook, run_shell_script  # Add the run_shell_script import
from .models import User, Log  # Add the Log import
from .email import send_email_to_admin  # Add this import for sending emails to the admin
from flask import request  # Add this import
from .logs import log_action
from .tokens import generate_token
from flask import jsonify

# Login Resource - Handles the login page rendering and authentication
class LoginResource(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('welcome'))
        return render_template('login.html')

    def post(self):
        # Get email and password from the request
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Verify the user's password and log them in if successful
        if user and user.verify_password(password):
            # Reset failed_attempts counter after successful login
            user.failed_attempts = 0
            user.save_to_db()
            login_user(user)
            return redirect(url_for('welcome'))
        else:
           if user:
                user.failed_attempts += 1
                # Check if failed_attempts reached 10
                if user.failed_attempts >= 10:
                    user.active = False
                    user.save_to_db()
                    log_action(user.id, 'Failed login - auto ban')
                    send_email_to_admin("User auto-banned", f"User {user.email} has been auto-banned after 10 failed login attempts.")
                    
                else:
                    user.save_to_db()
                    # Send a warning email after 5 failed attempts
                    if user.failed_attempts == 5:
                        send_email_to_admin("User failed 5 login attempts", f"User {user.email} has failed 5 login attempts.")
        return {'message': 'Invalid email or password'}, 401

# Registration Resource - Handles the registration page rendering and user registration
class RegistrationResource(Resource):
    def get(self):
        return render_template('register.html')

    def post(self):
        # Get email and password from the request
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User already exists'}, 400

        # Create a new user (without any roles) and commit to the database
        user = User(email=email, password=password)
        user.save_to_db()

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

        selected_get = request.form.get('selected_get')
        send_email_option = request.form.get('send_email')
        #return render_template('welcome.html', user_email=user_email, get_endpoints=get_endpoints)
        if selected_get in get_endpoints:
            # Check if the selected GET is a shell script or an Ansible playbook
            if selected_get.endswith('.sh'):
                # Execute the shell script
                output = run_shell_script(selected_get)
            else:
                # Execute the Ansible playbook
                output = run_playbook(selected_get)

            if send_email_option:
                # Send an email with the output to the user
                send_email("Playbook/Script Output", output, current_user.email)

            # Display the output on the welcome page
            return render_template('welcome.html', user_email=user_email, get_endpoints=get_endpoints, output=output)

        return {'message': 'Unauthorized GET request'}, 401
    
# BaseGetResource - Handles the GET request execution based on user roles
class BaseGetResource(Resource):
    role_required = None
    playbook_name = None

    @login_required
    def get(self):
        if self.role_required and not current_user.has_role(self.role_required):
            return {'message': 'Insufficient permissions'}, 403

        # Check if the selected GET is a shell script or an Ansible playbook
        if self.playbook_name.endswith('.sh'):
            # Execute the shell script
            output = run_shell_script(self.playbook_name)
        else:
            # Execute the Ansible playbook
            output = run_playbook(self.playbook_name)

        send_email("Playbook/Script Output", output, current_user.email)
# Log the user action
        log = Log(user_id=current_user.id, ip_address=request.remote_addr, action=f"Executed {self.playbook_name}")
        log.save_to_db()
        return {'message': 'Playbook or script executed and output sent via email'}

class GetUser1(BaseGetResource):
    role_required = 'Role1'
    playbook_name = 'playbook1'

class GetUser2(BaseGetResource):
    role_required = 'Role2'
    playbook_name = 'playbook2'

# Add more GET resources as needed

#Admin resource to view the logs
class AdminLogResource(Resource):
    @login_required
    def get(self):
        if not current_user.has_role("Admin"):
            return {'message': 'Unauthorized access'}, 403

        logs = Log.query.order_by(Log.timestamp.desc()).all()
        return render_template("admin_logs.html", logs=logs)
    
#Admin class that would allow the admin to ban the IPs
class AdminBanResource(Resource):
    @login_required
    def get(self):
        if not current_user.has_role("Admin"):
            return {'message': 'Unauthorized access'}, 403

        users = User.query.all()
        return render_template("admin_ban.html", users=users)

    @login_required
    def post(self):
        if not current_user.has_role("Admin"):
            return {'message': 'Unauthorized access'}, 403

        user_id = request.form.get('user_id')
        ban_action = request.form.get('ban_action')

        user = User.query.get(user_id)
        if user and ban_action == "ban":
            user.active = False
        elif user and ban_action == "unban":
            user.active = True
        user.save_to_db()

        users = User.query.all()
        return render_template("admin_ban.html", users=users)

class AdminUserResource(Resource):
    @login_required()
    @jwt_required()
    def get(self):
        if not current_user.has_role('Admin'):
            return {'message': 'Insufficient permissions'}, 403

        users = User.query.all()
        users_data = [{
            'id': user.id,
            'email': user.email,
            'roles': [role.name for role in user.roles],
            'token': user.token,
            'active': user.active
        } for user in users]

        return jsonify(users_data)

    @jwt_required()
    def post(self):
        if not current_user.has_role('Admin'):
            return {'message': 'Insufficient permissions'}, 403

        user_id = request.form.get('user_id')
        action = request.form.get('action')

        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, 404

        if action == 'reset_token':
            user.token = generate_token()
            user.save_to_db()
            return {'message': 'Token reset successfully'}
        else:
            return {'message': 'Invalid action'}, 400