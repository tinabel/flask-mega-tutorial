import os
basedir = os.path.abspath(os.path.dirname(__file__  ))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  TEST_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'test.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or \
    False

  LANGUAGES = ['en', 'es']

  MAIL_SERVER='smtp.sendgrid.net'
  MAIL_PORT=587
  MAIL_USE_TLS=1
  MAIL_USERNAME='apikey'
  MAIL_PASSWORD=os.environ.get('SENDGRID_API_KEY')
  MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')
  ADMINS=['tina@bellvance.com']

  POSTS_PER_PAGE = 25