from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .models import db
from .auth import auth_bp
from .routes import main


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Topher1212@localhost/personal_blog'
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main)

    return app
