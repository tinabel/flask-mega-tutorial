from config import Config
from flask import Flask, request
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os


app = Flask(__name__, static_folder='static/dist', static_url_path='')
app.config.from_object(Config)
babel = Babel(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
mail=Mail(app)
migrate = Migrate(app, db)
moment = Moment(app)

if not app.debug:
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
      toaddrs=app.config['ADMINS'], subject='Bell Vance Failure',
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

@babel.localeselector
def get_locale():
  return request.accept_languages.best_match(app.config['LANGUAGES'])

from app import routes, models, errors