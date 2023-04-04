from app import app, db, user_datastore
from app.models import User, Role

def init_db():
    # Create tables
    db.create_all()

    # Create Roles
    user_role = Role(name='User')
    admin_role = Role(name='Admin')

    # Add roles to the database
    db.session.add(user_role)
    db.session.add(admin_role)
    db.session.commit()

    # Create admin user
    admin_email = "admin@example.com"
    admin_password = "your_admin_password"

    user_datastore.create_user(email=admin_email, password=admin_password, roles=[admin_role])
    db.session.commit()

    print("Database initialized and admin user created.")

if __name__ == "__main__":
    with app.app_context():
        init_db()