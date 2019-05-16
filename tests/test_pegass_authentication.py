import pytest
from pytest_mock import mocker 

import mechanicalsoup

import crf_pegass_auth.pegass_authentication as pegass

def test_request_raise_exception_if_no_credentials_in_parameters():
    with pytest.raises(TypeError) as request_error:
        pegass.request('/crf/rest/unknown')
    assert str(request_error.value) == 'Missing either cookies or username/password to achieve the request'


def test_request_to_create_browser_with_default_user_agent(mocker):
    mocker.patch('mechanicalsoup.StatefulBrowser')
    pegass.request('/', cookies={'test': 'ok'})
    mechanicalsoup.StatefulBrowser.assert_called_once_with(user_agent=pegass.DEFAULT_USER_AGENT)


def test_request_to_create_browser_with_curstom_agent(mocker):
    mocker.patch('mechanicalsoup.StatefulBrowser')
    pegass.request('/', user_agent='custom_agent', cookies={'test': 'ok'})
    mechanicalsoup.StatefulBrowser.assert_called_once_with(user_agent='custom_agent')


def test_request_should_not_try_to_get_new_auth_if_cookies_provided(mocker):
    mocker.patch('mechanicalsoup.StatefulBrowser.get')
    mocker.patch.object(pegass, 'login')
    cookies = {'foo': 'bar'}
    pegass.request('foobar', cookies=cookies)
    mechanicalsoup.StatefulBrowser.get.assert_called_once_with('{}/foobar'.format(pegass.DEFAULT_PEGASS_URL), cookies=cookies)    
    assert not pegass.login.called


def test_request_should_get_new_auth_access_if_username_and_password_provided(mocker):
    mocker.patch('mechanicalsoup.StatefulBrowser.get')
    mocker.patch.object(pegass, 'login', return_value={'cookie': 'abcd1234'})
    credentials = { 'username': 'foo', 'password': 'bar' }
    pegass.request('foobar', username=credentials['username'], password=credentials['password'])
    mechanicalsoup.StatefulBrowser.get.assert_called_once_with('{}/foobar'.format(pegass.DEFAULT_PEGASS_URL), cookies={'cookie': 'abcd1234'})    
    pegass.login.assert_called_once_with(
        credentials['username'],
        credentials['password'],
        pegass.DEFAULT_PEGASS_URL,
        pegass.DEFAULT_AUTH_URL,
        pegass.DEFAULT_USER_AGENT)


def test_request_with_credentials_provided_should_be_callable_with_custom_pegass_urls(mocker):
    mocker.patch('mechanicalsoup.StatefulBrowser.get')
    mocker.patch.object(pegass, 'login', return_value={'cookie': 'abcd1234'})
    credentials = { 'username': 'foo', 'password': 'bar' }
    pegass.request('foobar', pegass_url='https://foo.bar.io', auth_url='https://foobar.auth.io', user_agent='custom_agent', username=credentials['username'], password=credentials['password'])
    mechanicalsoup.StatefulBrowser.get.assert_called_once_with('https://foo.bar.io/foobar', cookies={'cookie': 'abcd1234'})    
    pegass.login.assert_called_once_with(
        credentials['username'],
        credentials['password'],
        'https://foo.bar.io',
        'https://foobar.auth.io',
        'custom_agent')
