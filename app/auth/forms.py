from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
  # Returns a login form with a username, password, remember me, and submit field.
  #
  # Parameters:
  #   FlaskForm: The FlaskForm class.
  #
  # Returns:
  #   LoginForm: The login form.

  username = StringField(_l('Username'), validators=[DataRequired()])
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  remember_me = BooleanField(_l('Remember Me'))
  submit = SubmitField(_l('Sign In'))

class ResetPasswordRequestForm(FlaskForm):
  email = EmailField(_l('Email Address'), validators=[DataRequired(), Email()])
  submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField(_l('Reset Password'))

class RegistrationForm(FlaskForm):
  # Returns a registration form with a username, email, password, password2, and submit field.
  #
  # Parameters:
  #   FlaskForm: The FlaskForm class.
  #
  # Returns:
  #   RegistrationForm: The registration form.

  username = StringField(_l('Username'), validators=[DataRequired()])
  email = EmailField(_l('Email'), validators=[DataRequired(), Email()])
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  password2 = PasswordField(_l('Password Confirmation'), validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField(_l('Register'))

  def validate_username(self, username):
    # Checks if the username is unique.
    #
    # Parameters:
    #   username (str): The username to check.
    #
    # Returns:
    #   None

    user = User.query.filter_by(username=username.data).first()

    if user is not None:
      raise ValidationError(_l('Please use a different user name.'))

  def validate_email(self, email):
    # Checks if the user's email is unique.
    #
    # Parameters:
    #   email (str): The email to check.
    #
    # Returns:
    #   None

    user = User.query.filter_by(email=email.data).first()

    if user is not None:
      raise ValidationError(_l('Please use a different email address.'))