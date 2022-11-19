import re
from bs4 import BeautifulSoup


def get_csrftoken(html):
  str = next(BeautifulSoup(html, features="html.parser").find(
      attrs={'type': 'text/javascript'}).children
  )
  match = re.search(r'Anywhere.csrfToken = \"(\w+)\";', str)

  return match.group(1)


def get_session_data(session):
  print('[1/5] Getting initial session information')

  response = session.get('https://www.pythonanywhere.com/login/')

  csrftoken_html = get_csrftoken(response.content)

  return csrftoken_html
