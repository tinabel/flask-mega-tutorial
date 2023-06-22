from flask import render_template
from flask_mail import Message
from threading import Thread
from app import app, mail

def send_async_email(app, msg):
  # Sends an email asynchronously.
  #
  # Parameters:
  #   app (Flask): The Flask app.
  #   msg (Message): The message to send.
  #
  # Returns:
  #   None

  with app.app_context():
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
  # Sends an email.
  #
  # Parameters:
  #   subject (str): The subject of the email.
  #   sender (str): The sender of the email.
  #   recipients (list): The recipients of the email.
  #   text_body (str): The text body of the email.
  #   html_body (str): The HTML body of the email.
  #
  # Returns:
  #   None
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
  # Sends a password reset email.
  #
  # Parameters:
  #   user (User): The user to send the password reset email to.
  #
  # Returns:
  #   None
  token = user.get_reset_password_token()
  send_email(
    '[Tina Bell Vance] Reset Your Password',
    sender=app.config['MAIL_DEFAULT_SENDER'],
    recipients=[user.email],
    text_body=render_template('email/reset_password.txt', user=user, token=token),
    html_body=render_template('email/reset_password.html', user=user, token=token)
  )