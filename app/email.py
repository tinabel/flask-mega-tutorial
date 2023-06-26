from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail

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
  Thread(target=send_async_email, args=(current_app.get_current_object(), msg)).start()
