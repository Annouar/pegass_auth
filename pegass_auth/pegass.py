import os

import mechanicalsoup

DEFAULT_PEGASS_URL = 'https://pegass.croix-rouge.fr'
DEFAULT_AUTH_URL = 'https://id.authentification.croix-rouge.fr'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'


def login(username, password, pegass_url=DEFAULT_PEGASS_URL, auth_url=DEFAULT_AUTH_URL, user_agent=DEFAULT_USER_AGENT):
    browser = mechanicalsoup.StatefulBrowser(user_agent=user_agent)
    browser.open(auth_url)
    browser.select_form('form[action="/my.policy"]')
    browser['username'] = username
    browser['password'] = password
    browser['vhost'] = 'standard'

    browser.submit_selected()
    browser.open('{}/crf/rest'.format(pegass_url))

    browser.select_form('form[action="{}/Shibboleth.sso/SAML2/POST"]'.format(pegass_url))
    browser.submit_selected()

    cookies = browser.get_cookiejar().get_dict()
    return cookies


def request(url_to_call, pegass_url=DEFAULT_PEGASS_URL, auth_url=DEFAULT_AUTH_URL, user_agent=DEFAULT_USER_AGENT, **kwargs):
    browser = mechanicalsoup.StatefulBrowser(user_agent=user_agent)
    response = ''
    if 'cookies' in kwargs:
        response = browser.get('{}/{}'.format(pegass_url, url_to_call), cookies=kwargs['cookies']).json()
        browser.close()
        return response
    if 'username' in kwargs and 'password' in kwargs:
        auth_cookies = login(kwargs['username'], kwargs['password'], pegass_url, auth_url, user_agent)
        response = browser.get('{}/{}'.format(pegass_url, url_to_call), cookies=auth_cookies).json()
        browser.close()
        return response
    raise TypeError('Missing either cookies or username/password to achieve the request')


if __name__ == '__main__':
    username = os.environ['username']
    password = os.environ['password']
    auth_cookies = login(username, password)
    rules = request('crf/rest/gestiondesdroits', cookies=auth_cookies)
    print(rules)
