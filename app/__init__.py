import os
from flask import Flask
from flask_material import Material


from frontend import blueprint


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    # Front-end blueprint architecture of the app.
    Material(app)
    app.register_blueprint(blueprint)

    #SECRET_KEY must be overidden with random value for deploying.
    app.config.from_mapping(SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
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



    return app
