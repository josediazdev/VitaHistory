from flask import Flask
from vitahistory.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import pymysql


pymysql.install_as_MySQLdb()

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Para acceder se requiere iniciar sesión primero'
login_manager.login_message_category = 'info'

migrate = Migrate()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    migrate.init_app(app, db)



    from vitahistory.index import index
    app.register_blueprint(index)

    from vitahistory.auth import auth
    app.register_blueprint(auth)

    from vitahistory.person import person
    app.register_blueprint(person)

    from vitahistory.history import history
    app.register_blueprint(history)

    from vitahistory.error import error
    app.register_blueprint(error)


    return app
