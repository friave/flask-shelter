from flask import Flask
from flask_migrate import Migrate

from .extensions import db, ma
from .routes.animal import animals
from .routes.user import users


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    ma.init_app(app)
    # migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    migrate = Migrate(app,db)

    app.register_blueprint(users,  url_prefix="/users")
    app.register_blueprint(animals, url_prefix='/animals')

    return app
