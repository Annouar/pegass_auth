import os

import mechanicalsoup

PEGASS_URL = 'https://pegass.croix-rouge.fr/'
url_authentication = 'https://id.authentification.croix-rouge.fr'

def login():
  browser = mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0')
  browser.set_verbose(True)
  browser.open(url_authentication)
  print(browser.get_url())
  browser.select_form('form[action="/my.policy"]')
  browser['username'] = os.environ.get('LOGIN')
  browser['password'] = os.environ.get('PASSWORD')
  browser['vhost'] = 'standard'

  browser.submit_selected()
  browser.open('https://pegass.croix-rouge.fr/crf/rest')
  saml_response = browser.get_current_page().findAll('input', {'name': 'SAMLResponse'})[0].get('value')
  relay = browser.get_current_page().findAll('input', {'name': 'RelayState'})[0].get('value')

  browser.select_form('form[action="https://pegass.croix-rouge.fr/Shibboleth.sso/SAML2/POST"]')
  browser.submit_selected()

  cookies = browser.get_cookiejar().get_dict()
  print(cookies)

  return cookies

def request(url, cookies=None):
  browser = mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0')
  auth_cookies = cookies
  if cookies is None :  
    auth_cookies = login()
  return browser.get(url, cookies=auth_cookies).json()

print(request('https://pegass.croix-rouge.fr/crf/rest/gestiondesdroits'))



