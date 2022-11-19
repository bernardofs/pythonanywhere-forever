import os


def login(csrftoken_html, session):
  print('[2/5] Logging in')

  headers = {
    'Referer': 'https://www.pythonanywhere.com/login/',
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  username, password = os.getenv('PA_USERNAME'), os.getenv('PA_PASSWORD')
  data = f'csrfmiddlewaretoken={csrftoken_html}' \
      f'&auth-username={username}' \
      f'&auth-password={password}' \
      f'&login_view-current_step=auth'

  response = session.post('https://www.pythonanywhere.com/login/',
                          headers=headers, data=data)
