from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import User  # Assuming a User model exists
from database import db
from forms import CreateAdminForm, DeleteAccountForm

admin_bp = Blueprint('admin', __name__)

# Admin panel to view and delete users
@admin_bp.route('/admin')
def admin_panel():
    create_admin_form = CreateAdminForm()
    delete_account = DeleteAccountForm()

    if not session.get('username') or session.get('privilege') not in [1, 2]:
        flash("You must be logged in as an admin to access this page.")
        return redirect(url_for('auth.login'))

    # Fetch all users from the database (excluding the current admin user)
    users = User.query.filter(User.username != session['username']).all()

    return render_template(
        'admin.html',
        users=users,
        create_admin_form=create_admin_form,
        delete_account=delete_account
    )

# Route to delete a user account
@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('username') or session.get('privilege') not in [1, 2]:
        flash("You must be logged in as an admin to perform this action.")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    current_user_privilege = session.get('privilege')

    # Superadmin (privilege = 1) can delete users with privilege 0 or 2, but not other superadmins (privilege=1)
    if current_user_privilege == 1:
        if user.privilege == 1:
            flash("Superadmins cannot delete other superadmins.")
            return redirect(url_for('admin.admin_panel'))

    # Regular admin (privilege = 2) can delete only regular users (privilege = 0)
    elif current_user_privilege == 2:
        if user.privilege != 0:
            flash("Admins can only delete regular users.")
            return redirect(url_for('admin.admin_panel'))

    # If we get here, deletion is allowed
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.username} deleted successfully.")
    return redirect(url_for('admin.admin_panel'))
