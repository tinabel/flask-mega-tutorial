import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__  ))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  TEST_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'test.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or \
    False
  OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL')

  LANGUAGES = ['en', 'es']

  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = os.environ.get('MAIL_PORT')
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
  MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
  ADMIN = os.environ.get('SITE_ADMIN')

  POSTS_PER_PAGE = 25

  MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')