from flask import (
        render_template, Blueprint, flash, redirect,
        url_for, request, g, session
        )
from werkzeug.security import check_password_hash, generate_password_hash
from flask_material import Material
from database.db import get_db



blueprint = Blueprint('blueprint', __name__)



@blueprint.route('/')
def index():

    return 'Hello World!'




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
                'INSERT INTO user (firstname, lastname, email, password) VALUES (?, ?, ?, ?)',
                (firstname, lastname, email, generate_password_hash(password))
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
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blueprint.index'))

        flash(error)

    return render_template('login.html')




@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blueprint.index'))




@blueprint.before_app_request
def loadLoggedUser():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
