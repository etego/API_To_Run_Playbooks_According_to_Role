# API GET and RUN

This project demonstrates a scalable Flask-RESTful API with user roles, authentication, and email notifications for running playbooks.

## Capabilities
- User authentication:

-- Login page for existing users to enter their email and password.
-- Registration page for new users to register with their email and password.

- Role-based access control:

-- Different user roles with specific GET endpoints allowed for each role.
-- Restricts access to GET endpoints based on the user's role.

- GET request execution:

-- Executes Ansible playbooks or shell scripts based on the selected GET endpoint.
-- Returns the output of the playbook or shell script execution.

- Email notifications:

-- Sends the output of the playbook or shell script execution via email to the user.
-- Triggers GET requests via email.
-- Sends a warning email to the admin when a login fails more than 5 times.

- Admin interface:

-- Approve or decline user registration requests.
-- View and manage all users and their roles.
-- View logs of user actions, including time and IP address.
-- Ban users or IP addresses manually.
-- Automatically ban users or IP addresses after 10 failed login attempts.
-- View user tokens and passwords.
-- Generate new tokens for users.
-- Register and store user, role, password, and token information in a MySQL database.

- Security features:

-- Strong authentication mechanism for the admin interface.
-- JWT for API authentication and access control.
-- IP-based banning to prevent brute force attacks.
-- Logging of user actions for security monitoring and auditing purposes.

## Content
.
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── playbooks.py
│   ├── email.py
│   ├── resources.py
│   ├── routes.py
│   └── templates
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       └── welcome.html
├── config.py
├── db_create.py
├── requirements.txt
├── run.py
└── README.md

__init__.py: This file initializes the Flask app, the database, and Flask-JWT-Extended.
models.py: Contains the database models for User and Role.
playbooks.py: Contains the functions to execute Ansible playbooks.
email.py: Contains functions for sending emails.
resources.py: Contains the Flask-RESTful resources for handling login, registration, and the welcome page.
routes.py: Configures the routes for the app's resources.
templates: Contains the HTML templates for the login, registration, and welcome pages.
config.py: Contains the configuration settings for the Flask app.
db_create.py: Script to create the database and an admin user.
requirements.txt: Lists the required Python packages for the project.
run.py: The main script to run the Flask app.
README.md: Provides a brief explanation of the project, its setup, and usage.

## Requirements

- Python 3.6+
- Ansible
- A working email server (e.g., Gmail, SendGrid)

## Setup

1. Install dependencies:

Flask: The main framework for building the web application.
Flask-RESTful: An extension for building RESTful APIs with Flask.
Flask-SQLAlchemy: An extension for using SQLAlchemy with Flask to interact with the database.
Flask-Security-Too: An extension providing security features such as user authentication, registration, and role management.
Flask-Admin: An extension for creating an admin interface for managing users and roles.
Flask-Mail: An extension for sending emails using the Flask framework.
passlib: A library for password hashing and verification.

```
pip install -r requirements.txt
```

2. Initialize the database and create an admin user:

```
python db_init.py
```

3. Run the Flask application:
```
python run.py
```
4. Run the email scheduler
```
python scheduler.py
```
Now, the script will check the email inbox every minute and process any unread emails from the allowed senders. If the subject of an email matches a GET request (e.g., "get1" or "get2"), it will run the corresponding playbook and send the output via email to the sender.

Keep in mind that you should use a separate email address for the API to avoid mixing personal emails with emails related to the API. When an allowed sender sends an email to trigger a GET request, they must include their unique token in the email body. If the token is not present or invalid, the request will not be processed. This adds an extra layer of security to prevent unauthorized access to the GET requests.

5. Generate email tokes with
```
python generate_tokens.py
```

## Usage

- Access the admin interface at `/admin` to manage users and roles.
- Use the `/login`, `/register`, and `/get{N}` endpoints to interact with the API.

## Adding New GET Requests and Playbooks

1. Add new playbook functions in `playbooks.py`.
2. Update the `allowed_gets` field of the corresponding role in the database.
3. Extend the `BaseGetResource` class in `resources.py`.
4. Set the `role_required` and `playbook_name` attributes.
5. Register the new resource in `routes.py`.

## Running the Project

1. Start the Flask app: `python run.py`
2. Navigate to the login page (e.g., http://localhost:5000/login) in your web browser.
3. Register new users and assign roles.
4. Use the welcome page to execute GET requests and view playbook output.


## Email Triggering

1. Generate tokens for allowed senders using the `generate_tokens.py` script.
2. Update the `TOKENS` dictionary in the `scheduler.py` script.
3. Configure the scheduler to run at the desired interval.
4. Ensure the email server settings are correct in `config.py` and `email.py`.

Emails should be formatted as follows to trigger GET requests:

Subject: `Execute {GET_NAME}`
Body: `Token: {TOKEN}`