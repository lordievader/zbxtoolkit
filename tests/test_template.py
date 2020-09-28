#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Tests for the functions of zbxtoolkit.
"""
import pytest
import pdb
from zbxtoolkit import templates


def test_template(mocker):
    """Tests the template function.
    """
    mocker.patch.object(templates, 'init')
    zapi = mocker.MagicMock()
    templates.template('Test')
    templates.template('Test', zapi)
    zapi.template.get.assert_called_with(filter={'name': 'Test'})

    zapi.template.get.return_value = []
    with pytest.raises(RuntimeError) as excinfo:
        templates.template('Test', zapi)
        assert 'Test' in str(excinfo.value)


def test_template_id(mocker):
    """Tests the template_id function.
    """
    mocker.patch.object(templates, 'template', return_value={'templateid': 1})
    assert templates.template_id('Test') == 1


def test_template_create(mocker):
    """Tests the creation of a template.
    """
    class Group:  # pylint: disable=too-few-public-methods
        """Mock class for the group attribute.
        """
        groupid = 1

    zapi = mocker.MagicMock()
    zapi.template = mocker.MagicMock()
    with pytest.raises(RuntimeError) as excinfo:
        templates.template_create('Test', {}, zapi=zapi)
        assert 'groupid' in str(excinfo.value)

    group = Group()
    templates.template_create('Test', group, zapi=zapi)
    # TODO: fix this assertion
    # assert zapi.template.create.assert_called_with(
    #     host='Test', groups=group
    # )
