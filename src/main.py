import requests
import time
import traceback
from .get_session_data import get_session_data
from .login import login
from .move_to_web import move_to_web
from .renew_period import renew_period
from .send_email_sendgrid import send_error_message, send_success_message

# Execute the logic for the renewal for [TRIES] times. If it succedes,
# send an email with a success message, otherwise send an error message.


def execute():
  TRIES = 3

  for tries in range(1, TRIES + 1):
    print(f'Attempt {tries}')

    try:
      session = requests.Session()

      csrftoken_html = get_session_data(session)

      login(csrftoken_html, session)

      csrftoken_html = move_to_web(session)

      renew_period(csrftoken_html, session)

      send_success_message()

    except Exception:
      print('An error has occurred')
      traceback.print_exc()
      if tries != TRIES:
        # Wait a little bit until execute the scrapping again.
        time.sleep(60)

    else:
      return 'The script was successfully executed!'

  send_error_message()
  return 'An error has occurred .'
