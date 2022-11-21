import os

# Renew the period the website will be running for more 3 months.


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

  if response.status_code == 200 and response.url == f'https://www.pythonanywhere.com/user/{username}/webapps/':
    print('Success!')
  else:
    raise Exception('Error while trying to renew the period.')
