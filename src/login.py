import os

# Login into pythonanywhere using the username and password.


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

  if response.url != f'https://www.pythonanywhere.com/user/{username}/':
    raise Exception(
      'The program couldn\'t login. Please check the username and password.'
    )
