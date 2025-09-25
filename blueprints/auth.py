from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
from forms import LoginForm, RegisterForm, logoutForm, changePasswordForm, DeleteAccountForm, CreateAdminForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['username'] = form.username.data
            session['privilege'] = user.privilege
            return redirect(url_for('home.home_page'))
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=16)
        new_user = User(username=form.username.data, password_hash=hashed_password, privilege=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login', form=form))
    return render_template('register.html', form=form)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    form = logoutForm()
    session.clear()
    return redirect(url_for('auth.login', form=form))

@auth_bp.route('/delete_account', methods=['POST'])
def delete_account():
    if not session.get('username'):
        flash('You need to be logged in to delete your account.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['username']).first()

    if not user:
        flash("User not found.")
        return redirect(url_for('account.account'))  # Redirect back to account if user is not found

    # Delete user from the database
    db.session.delete(user)
    db.session.commit()
    session.clear()  # Clear the session after deletion

    flash("Your account has been successfully deleted.")
    return redirect(url_for('auth.login'))  # Redirect to login page

@auth_bp.route('/registerAdmin', methods=['POST'])
def register_admin():
    create_admin_form = CreateAdminForm()

    username = create_admin_form.username.data
    password = create_admin_form.password.data

    if User.query.filter_by(username=username).first():
        flash('Username already exists.')
        return redirect(url_for('admin.admin_panel'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    new_admin = User(username=username, password_hash=hashed_password, privilege=2)

    db.session.add(new_admin)
    db.session.commit()

    flash('Admin account created successfully!')
    return redirect(url_for('admin.admin_panel'))


@auth_bp.route('/change_password', methods=['POST'], endpoint='auth_change_password')
def change_password():
    form = changePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=session.get('username')).first()
        if user and check_password_hash(user.password_hash, form.old_password.data):
            user.password_hash = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash("Your password has been updated.")
        else:
            flash("Current password is incorrect.")
    
    return redirect(url_for('account.account'))  # Redirect back to the account page


@auth_bp.route('/change_password', methods=['POST'])
def change_password():
    form = changePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=session.get('username')).first()
        if user and check_password_hash(user.password_hash, form.old_password.data):
            user.password_hash = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash("Your password has been updated.")
        else:
            flash("Current password is incorrect.")
    
    return redirect(url_for('account.account'))  # Redirect back to the account page
