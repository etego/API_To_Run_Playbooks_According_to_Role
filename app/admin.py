from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required, current_user
from .models import User, Role
from . import user_datastore

app = Blueprint('admin', __name__, template_folder='templates')

@app.route('/admin')
@login_required
def admin():
    if not current_user.has_role('Admin'):
        return {'message': 'Insufficient permissions'}, 403

    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/admin/update_role', methods=['POST'])
@login_required
def update_role():
    if not current_user.has_role('Admin'):
        return {'message': 'Insufficient permissions'}, 403

    user_id = request.form.get('user_id')
    new_role = request.form.get('new_role')

    user = User.query.get(user_id)
    if not user:
        return {'message': 'User not found'}, 404

    # Remove all roles from the user
    for role in user.roles:
        user_datastore.remove_role_from_user(user, role)
    user_datastore.commit()

    # Assign the new role to the user
    user_datastore.add_role_to_user(user, new_role)
    user_datastore.commit()

    return redirect(url_for('admin'))
