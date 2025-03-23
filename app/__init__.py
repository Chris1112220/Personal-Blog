from flask import Flask
from .routes import main  # import the blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # attach the routes
    return app
