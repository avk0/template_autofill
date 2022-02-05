""" This is a copy from https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/"""

import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
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
