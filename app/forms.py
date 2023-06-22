from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
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

class EditProfileForm(FlaskForm):
  # Returns a form to edit the user's profile.
  #
  # Parameters:
  #   FlaskForm: The FlaskForm class.
  #
  # Returns:
  #   EditProfileForm: The edit profile form.

  username = StringField(_l('Username'), validators=[DataRequired()])
  first_name = StringField(_l('First Name'), validators=[Length(min=0, max=64)], default='')
  middle_name = StringField(_l('Middle Name'), validators=[Length(min=0, max=64)], default='')
  last_name = StringField(_l('Last Name'), validators=[Length(min=0, max=64)], default='')
  about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
  submit = SubmitField(_l('Save'))

  def __init__(self, original_username, *args, **kwargs):
    # Initializes the edit profile form.
    #
    # Parameters:
    #   original_username (str): The original username.
    #   *args: Variable length argument list.
    #   **kwargs: Arbitrary keyword arguments.
    #
    # Returns:
    #   None

    super(EditProfileForm, self).__init__(*args, **kwargs)
    self.original_username = original_username

  def validate_username(self, username):
    if username.data != self.original_username:
      user = User.query.filter_by(username=self.username.data).first()

      if user is not None:
        raise ValidationError(_l('Please use a different username.'))

class EmptyForm(FlaskForm):
  submit = SubmitField('Submit')

class PostForm(FlaskForm):
  # Returns a form to create a post.
  #
  # Parameters:
  #   FlaskForm: The FlaskForm class.
  #
  # Returns:
  #   PostForm: The post form.

  post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1)])
  title = StringField(_l('Post Title'), validators=[DataRequired(), Length(min=1, max=120)])
  submit = SubmitField(_l('Submit'))