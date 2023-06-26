import jwt
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import check_password_hash, generate_password_hash
from time import time
from app import db, login

followers = db.Table(
  'followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

class User(UserMixin, db.Model):
  # This class represents a user.
  #
  # Parameters:
  #  UserMixin: The UserMixin class.
  #  db.Model: The db.Model class.
  #
  # Returns:
  #  User: The user with the given id.
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  first_name = db.Column(db.String(64))
  middle_name = db.Column(db.String(64))
  last_name = db.Column(db.String(64))
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)

  followed = db.relationship(
    'User',
    secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'),
    lazy='dynamic'
  )

  def __repr__(self):
    # Returns a string representation of the user.
    #
    # Parameters:
    #  None
    #
    # Returns:
    #  str: The string representation of the user.

    return '<User {}>'.format(self.username)

  def set_password(self, password):
    # Sets the password hash of the user.
    #
    # Parameters:
    #  password (str): The password to hash.
    #
    # Returns:
    #  None
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    # Checks if the given password matches the password hash.
    #
    # Parameters:
    #  password (str): The password to check.
    #
    # Returns:
    #  bool: True if the password matches, False otherwise.

    return check_password_hash(self.password_hash, password)

  def avatar(self, size):
    # Returns the avatar of the user.
    #
    # Parameters:
    #  size (int): The size of the avatar.
    #
    # Returns:
    #  str: The avatar of the user.

    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

  def full_name(self):
    # Returns the full name of the user.
    #
    # Parameters:
    #  None
    #
    # Returns:
    #  str: The full name of the user.

    return ' '.join(list(filter(None, [self.first_name, self.middle_name, self.last_name])))

  def first_and_last_name(self):
    # Returns the first and last name of the user.
    #
    # Parameters:
    #  None
    #
    # Returns:
    #  str: The full name of the user.

    return ' '.join(list(filter(None, [self.first_name, self.last_name])))

  def follow(self, user):
    # Follows the given user.
    #
    # Parameters:
    #  user (User): The user to follow.
    #
    # Returns:
    #  None

    if not self.is_following(user):
      self.followed.append(user)

  def unfollow(self, user):
    # Unfollows the given user.
    #
    # Parameters:
    #  user (User): The user to unfollow.
    #
    # Returns:
    #  None

    if self.is_following(user):
      self.followed.remove(user)

  def is_following(self, user):
    # Checks if the user is following the given user.
    #
    # Parameters:
    #  user (User): The user to check.
    #
    # Returns:
    #  bool: True if the user is following the given user, False otherwise.

    return self.followed.filter(followers.c.followed_id == user.id).count() > 0

  def followed_posts(self):
    # Returns the posts of the users that the user is following as well as the user's own posts.
    #
    # Parameters:
    #  None
    #
    # Returns:
    #  list: The posts of the users that the user is following as well as the user's own posts.

    followed = Post.query.join(
      followers, (followers.c.followed_id == Post.user_id)).filter(
        followers.c.follower_id == self.id)

    own = Post.query.filter_by(user_id=self.id)
    return followed.union(own).order_by(Post.timestamp.desc())

  def get_reset_password_token(self, expires_in=600):
    # Returns a reset password token for the user.
    #
    # Parameters:
    #  expires_in (int): The time in seconds for the token to expire.
    #
    # Returns:
    #  str: The reset password token for the user.

    return jwt.encode(
      {'reset_password': self.id, 'exp': time() + expires_in},
      current_app.config['SECRET_KEY'], algorithm='HS256'
    )

  @staticmethod
  def verify_reset_password_token(token):
    # Verifies the given reset password token.
    #
    # Parameters:
    #  token (str): The reset password token to verify.
    #
    # Returns:
    #  User: The user associated with the given reset password token.

    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
    except:
      return

    return User.query.get(id)

@login.user_loader
def load_user(id):
  # Returns the user with the given id.
  #
  # Parameters:
  #  id (int): The id of the user to return.
  #
  # Returns:
  #  User: The user with the given id.
  return User.query.get(int(id))

class Post(db.Model):
  # This class represents a post.
  #
  # Parameters:
  #  db.Model: The db.Model class.
  #
  # Returns:
  #  Post: The post with the given id.

  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)
  language = db.Column(db.String(5))
  title = db.Column(db.String(120))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    # Returns a string representation of the post.
    #
    # Parameters:
    #  None
    #
    # Returns:
    #  str: The string representation of the post.

    return'<Post {}>'.format(self.body)
