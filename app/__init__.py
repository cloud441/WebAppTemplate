import os
from flask import Flask, url_for
from flask_material import Material
from flask_debug import Debug


from frontend import blueprint
import database.db as db


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    Debug(app)

    # Front-end blueprint architecture of the app.
    Material(app)
    app.register_blueprint(blueprint)

    APP_SECRET_KEY = os.urandom(32)
    app.config.from_mapping(SECRET_KEY=APP_SECRET_KEY,
            DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
            FLASK_DEBUG_DISABLE_STRICT='True',
            )
    app.debug = True


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #Database managment
    with app.app_context():
        db.init_app(app)


    return app
