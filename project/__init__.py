from flask import Flask
from flask_migrate import Migrate

from .extensions import db
from .routes.animal import animal
from .routes.main import main
from .routes.api import api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    # migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    migrate = Migrate(app,db)

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(animal, url_prefix='/animal')

    return app
