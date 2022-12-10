from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.LocalConfig')

    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():

        from . import routes
        db.create_all()

    return app
