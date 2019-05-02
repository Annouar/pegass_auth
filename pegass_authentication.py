import os

import mechanicalsoup

PEGASS_URL = 'https://pegass.croix-rouge.fr'
URL_AUTHENTICATION = 'https://id.authentification.croix-rouge.fr'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'


class PegassClient:
    def __init__(self, pegass_url=PEGASS_URL, url_authentication=URL_AUTHENTICATION, user_agent=DEFAULT_USER_AGENT):
        self.pegass_url = pegass_url
        self.url_authentication = url_authentication
        self.user_agent = user_agent

    def login(self, username, password):
        browser = mechanicalsoup.StatefulBrowser(user_agent=self.user_agent)
        browser.open(self.url_authentication)
        browser.select_form('form[action="/my.policy"]')
        browser['username'] = username
        browser['password'] = password
        browser['vhost'] = 'standard'

        browser.submit_selected()
        browser.open('https://pegass.croix-rouge.fr/crf/rest')

        browser.select_form('form[action="{}/Shibboleth.sso/SAML2/POST"]'.format(self.pegass_url))
        browser.submit_selected()

        cookies = browser.get_cookiejar().get_dict()
        return cookies

    def request(self, url_to_call, cookies=None):
        browser = mechanicalsoup.StatefulBrowser(user_agent=self.user_agent)
        auth_cookies = cookies
        if cookies is None:
            auth_cookies = self.login()
        return browser.get('{}/{}'.format(self.pegass_url, url_to_call), cookies=auth_cookies).json()


if __name__ == '__main__':
    client = PegassClient()
    auth_cookies = client.login(os.environ.get('username'), os.environ.get('password'))
    rules = client.request('crf/rest/gestiondesdroits', cookies=auth_cookies)
    print(rules)
