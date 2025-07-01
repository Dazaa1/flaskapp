import os

from flask import Flask

# application factory
def create_app(test_config=None):
    # create and configure the app
    # and the configuration files should be relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)

    # some default config
    # SECRET_KEY = dev meaning we are in dev not production, just to provide a convenient value during dev, and it is used by flask and extensions to make sure data is safe,
    # and should be overriden when deploying
    # database is where the sqlite file is located and it is in app.instance_path which is where flask decided to put instance folder
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    # it is a route that creates a connection between url /hello and a function that returns a response 'Hello, World!'
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app