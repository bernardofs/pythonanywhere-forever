import os
from .get_session_data import get_csrftoken


def move_to_web(session):
  print('[3/5] Move to \"web\" page')

  username = os.getenv('PA_USERNAME')
  headers = {
    'Referer': f'https://www.pythonanywhere.com/user/{username}/'
  }

  response = session.get(f'https://www.pythonanywhere.com/user/{username}/webapps/',
                         headers=headers)

  csrftoken_html = get_csrftoken(response.content)

  return csrftoken_html
