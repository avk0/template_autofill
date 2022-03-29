""" This is a copy from https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/"""

import os

from flask import Flask



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dfgdf65gfdg45k.12scd89.vgds22gyj888e22xcdr7895fgf'

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
        logs_folder = os.path.join(app.instance_path, 'log')
        os.makedirs(logs_folder, exist_ok=True)
    except OSError:
        pass

    # a simple test page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    with app.app_context():
        from template_autofill import routes
        app.register_blueprint(routes.bp)

    return app
