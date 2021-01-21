from flask import (
        render_template, Blueprint, flash, redirect,
        url_for, request, g, session
        )
from werkzeug.security import check_password_hash, generate_password_hash
from flask_material import Material
from flask_login import login_required, login_user, logout_user


from database.db import get_db
from login import Logger, login_manager



blueprint = Blueprint('blueprint', __name__)



@blueprint.route('/')
@login_required
def index():
    return render_template('index.html')




@blueprint.route('/register', methods = ['GET', 'POST'])
def register():

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'
        elif not email:
            error = 'Email address is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (firstname, lastname, email, password, active) VALUES (?, ?, ?, ?, ?)',
                (firstname, lastname, email, generate_password_hash(password), 1)
            )
            db.commit()
            return redirect(url_for('blueprint.login'))

        flash(error)

    return render_template('register.html')




@blueprint.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            logger_user = load_user(user['id'])
            login_user(logger_user)
            return redirect(url_for('blueprint.index'))

        flash(error)

    return render_template('login.html')




@blueprint.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('blueprint.login'))




@login_manager.user_loader
def load_user(id):
    db = get_db()
    user = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()

    return Logger(user['firstname'],user['id'],user['active'])
