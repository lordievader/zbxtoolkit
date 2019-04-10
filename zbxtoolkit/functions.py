#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <o.i.vandertoorn@utwente.nl>
Description:    Zabbix API functions.
"""
import logging
import os
import pdb  # noqa: F401
import json
import yaml
import dns.resolver
from pyzabbix import ZabbixAPI


def remove_non_primary(groupname=None, zapi=None):
    """Removes all non primary interfaces.

    :param groupname: name of the group to use
    :type groupname: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    """
    if zapi is None:
        zapi = init()

    if groupname is not None:
        group_id = groupid(groupname, zapi=zapi)

    else:
        group_id = None

    for host in zapi.host.get(groupids=group_id):
        interfaces = zapi.hostinterface.get(hostids=host['hostid'])
        delete = []
        for interface in interfaces:
            if interface['main'] == '0':
                delete.append(interface['interfaceid'])

        for interfaceid in delete:
            zapi.hostinterface.delete(interfaceid)


def resolve(hostname, qtype):
    """Resolver.
    """
    response = dns.resolver.query(hostname, qtype)
    answer = None
    if response:
        try:
            answer = response.response.answer[0].items[0].address

        except:
            pass

    return answer

def read_config():
    """Read a zabbix-matrix config file.

    :param config_file: config file to read
    :type config_file: str
    :param section: section to read from the config file
    :type section: str
    :return: config dictionary
    """
    path = 'zapi.yml'
    if os.path.isfile(path) is False:
        logging.error('config file "%s" not found', path)

    with open(path, 'r') as config_file:
        data = yaml.load(config_file, Loader=yaml.Loader)

    return data


def init(config=None):
    """Initializes the ZabbixAPI with the config.

    :param config: config to use, as returned by read_config
    :type config: dict
    :return: ZabbixAPI reference
    """
    if config is None:
        config = read_config()

    logging.debug(config)
    zapi = ZabbixAPI(config['host'])
    zapi.login(config['username'], config['password'])
    return zapi


def group(groupname, zapi=None):
    """Gathers the group with a given name.

    :param groupname: name of the group (exact match)
    :type groupname: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: the group (dict)
    """
    if zapi is None:
        zapi = init()

    for group in zapi.hostgroup.get():
        if group['name'] == groupname:
            break

    else:
        raise RuntimeError(f'Group {groupname} not found.')

    return group


def groupid(groupname, zapi=None):
    """Gathers the group ID with a given name.

    :param groupname: name of the group
    :type groupname: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: the groupid (str)
    """
    return group(groupname, zapi)['groupid']

def template(templatename, zapi=None):
    """Gathers a template with a given name.

    :param templatename: name of the template (fuzzy match)
    :type templatename: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: the template (dict)
    """
    if zapi is None:
        zapi = init()

    for template in zapi.template.get():
        if templatename in  template['name']:
            break

    else:
        raise RuntimeError(f'Template {templatename} not found.')

    return template


def templateid(templatename, zapi=None):
    """Gathers the template ID with a give name.

    :param templatename: name of the template
    :type templatename: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: the templateid (str)
    """
    return template(templatename, zapi)['templateid']


def group_member(host, groupname, zapi=None):
    """Checks if the host is a member of the given group.

    :param host: host dictionary
    :type host: dict
    :param groupname: name of the group
    :type groupname: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: group membership status (boolean)
    """
    if zapi is None:
        zapi = init()

    groups = zapi.hostgroup.get(hostids=host['hostid'])
    return groupname in [group['name'] for group in groups]


def hosts_in_group(groupname, zapi=None):
    """Returns all the hosts from a group.

    :param groupname: name of the group
    :type groupname: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: group membership status (boolean)
    """
    if zapi is None:
        zapi = init()

    return zapi.host.get(groupids=groupid(groupname))


def main_interface(host, zapi=None):
    """Retrieves the main interface.

    :param host: host dictionary
    :type host: dict
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: main interface
    """
    if zapi is None:
        zapi = init()

    for interface in zapi.hostinterface.get(hostids=host['hostid']):
        if interface['main'] == 1:
            break

    return interface


def interface_exists(host, interface, zapi=None):
    """Checks if the interface already exists.
    It checks if the 'useip', 'ip' and 'dns' fields are the same.

    :param host: host dictionary
    :type host: dict
    :param interface: interface dictionary
    :type interface: boolean
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: interface exists (boolean)
    """
    if zapi is None:
        zapi = init()

    check = ['useip', 'ip', 'dns']
    interfaces = zapi.hostinterface.get(hostids=host['hostid'])
    exist = False
    for compare in interfaces:
        set_A = []
        set_B = []
        for item in check:
            set_A.append(str(interface[item]))
            set_B.append(str(compare[item]))

        if set(set_A) == set(set_B):
            exist = True
            break

    return exist
