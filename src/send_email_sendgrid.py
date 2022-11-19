import sendgrid
import os
from sendgrid.helpers.mail import *


def gen_success_message():
  subject = 'The pythonanywhere period was renewed'
  body = 'The website will be alive for more 3 months'
  return subject, body


def send_success_message():
  print('[5/5] Sending success message')

  sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

  subject, body = gen_success_message()

  mail = Mail(Email(os.getenv('SENDER_EMAIL')), To(
      os.getenv('RECIPIENT_EMAIL')
  ), subject, body)

  sg.client.mail.send.post(request_body=mail.get())


def send_error_message():
  print('[ERROR] Sending error message')
  sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

  subject = 'The pythonanywhere period couldn\'t be extended'

  body = f'An error has ocurred after trying to extend the pythonanywhere period. ' \
      f'Please, try to do it manually.'

  mail = Mail(Email(os.getenv('SENDER_EMAIL')), To(
      os.getenv('RECIPIENT_EMAIL')
  ), subject, body)
  sg.client.mail.send.post(request_body=mail.get())
