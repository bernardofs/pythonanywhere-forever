import sendgrid
import os
from sendgrid.helpers.mail import *

# Contains all logic for sending success/error messages via email.


username = os.getenv('PA_USERNAME')


def send_message(sg, subject, body):
  mail = Mail(Email(os.getenv('SENDER_EMAIL')), To(
      os.getenv('RECIPIENT_EMAIL')
  ), subject, body)
  sg.client.mail.send.post(request_body=mail.get())


def send_success_message():
  print('[5/5] Sending success message')

  sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

  subject = f'The period of your \"{username}\" pythonanywhere website was renewed'
  body = 'Your website will be running for more 3 months from now!'

  send_message(sg, subject, body)


def send_error_message():
  print('[ERROR] Sending error message')

  sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

  subject = f'The pythonanywhere period from \"{username}\" couldn\'t be extended'
  body = f'An error has ocurred while trying to extend the period. ' \
      f'Please, try to do it manually.'

  send_message(sg, subject, body)
