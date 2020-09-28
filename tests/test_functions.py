#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Tests for the functions of zbxtoolkit.
"""
from zbxtoolkit import functions

CONFIG = {
    'host': 'https://zabbix.example.nl/',
    'username': 'user',
    'password': 'password'
}


def test_read_config():
    """Tests the read_config function.
    """
    path = './tests/zapi.yml'
    assert functions.read_config(path) == CONFIG


def test_init(mocker):
    """Tests the init function.
    """
    mocker.patch.object(functions, 'read_config', return_value=CONFIG)
    mocker.patch.object(functions, 'ZabbixAPI')
    zapi = functions.init(CONFIG)
    assert isinstance(zapi, mocker.MagicMock)
    zapi.login.assert_called_with(CONFIG['username'], CONFIG['password'])

    zapi = functions.init()
    assert isinstance(zapi, mocker.MagicMock)
    zapi.login.assert_called_with(CONFIG['username'], CONFIG['password'])
