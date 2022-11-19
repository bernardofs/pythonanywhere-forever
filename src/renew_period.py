import os


def renew_period(csrftoken_html, session):
  print('[4/5] Renew period up to 3 months')

  username = os.getenv('PA_USERNAME')
  headers = {
    'Referer': f'https://www.pythonanywhere.com/user/{username}/webapps/',
    'Content-Type': 'application/x-www-form-urlencoded',
  }

  data = f'csrfmiddlewaretoken={csrftoken_html}'

  response = session.post(
      f'https://www.pythonanywhere.com/user/{username}/webapps/{username}.pythonanywhere.com/extend',
      headers=headers, data=data
  )

  if response.status_code == 200:
    print('Success!')
  else:
    raise Exception('Error: Status code different from 200')
