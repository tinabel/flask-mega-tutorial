import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
from config import Config
from opensearchpy import OpenSearch
from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
moment = Moment()
babel = Babel()

def create_app(config_class=Config):
  # Creates the application.
  #
  # Parameters:
  #   config_class (Config): The configuration class to use.
  #
  # Returns:
  #   Flask: The application.
  #
  # Note:
  #   This function is called by the Flask CLI.

  app = Flask(__name__, static_folder='static/dist', static_url_path='')
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  login.init_app(app)
  mail.init_app(app)
  moment.init_app(app)
  babel.init_app(app)
  app.opensearch = OpenSearch([app.config['OPENSEARCH_URL']]) if app.config['OPENSEARCH_URL'] else None

  from app.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp, url_prefix='/auth')

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  if not app.debug and not app.testing:
    # Email logging
    if app.config['MAIL_SERVER']:
      auth = None
      if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
      secure = None
      if app.config['MAIL_USE_TLS']:
        secure = ()
      mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr= app.config['MAIL_DEFAULT_SENDER'],
        toaddrs=app.config['ADMIN'], subject='Bell Vance Failure',
        credentials=auth, secure=secure
      )
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)

    # File logging
    if not os.path.exists('logs'):
      os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/bellvance.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
      logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
      )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')

  return app

@babel.localeselector
def get_locale():
  return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from app import models