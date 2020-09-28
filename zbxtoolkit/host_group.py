#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Zabbix API functions regarding host groups.
"""
import logging
import pdb  # noqa: F401
from pyzabbix import ZabbixAPI
from .functions import init


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

    return zapi.host.get(groupids=groupid(groupname, zapi=zapi))
