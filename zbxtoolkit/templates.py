#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Zabbix API functions regarding templates.
"""
import logging
import pdb  # noqa: F401
from pyzabbix import ZabbixAPI
from .functions import init


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

    _template = zapi.template.get(filter={'name': templatename})
    if not _template:
        raise RuntimeError(f'Template {templatename} not found.')

    return _template


def template_id(templatename, zapi=None):
    """Gathers the template ID with a give name.

    :param templatename: name of the template
    :type templatename: str
    :param zapi: reference to the ZabbixAPI
    :type zapi: ZabbixAPI
    :returns: the templateid (str)
    """
    return template(templatename, zapi)['templateid']


def template_create(name, groups, zapi=None):
    """Creates a template.

    :param name: the name for the template
    :type name: str
    :param groups: host groups to add the template to (required)
    :type groups: dict, must have the `groupid` property defined
    :return: the template
    """
    if 'groupid' not in dir(groups):
        raise RuntimeError("Groups must have the `groupid` property defined")

    if zapi is None:
        zapi = init()

    _template = zapi.template.create(
        host=name,
        groups=groups,
    )
    return _template
