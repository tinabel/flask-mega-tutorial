from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

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