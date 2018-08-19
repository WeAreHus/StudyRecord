##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Utilities for testing form machinery

$Id$
"""
from zope.interface.interfaces import IMethod
from zope.security.interfaces import ForbiddenAttribute, Unauthorized
import zope.security.checker
from zope.schema import getFieldsInOrder

class DummyChecker(object):
    """a checker for testing that requires explicit declarations

    requires explicit declaration of what is and is not authorized; does not
    require testing machinery to set up an interaction or a request.

    To instantiate, pass two dictionaries, the first for get access attribute
    protection, and the second for set access attribute protection.  keys
    should be the attribute names, and values should be boolean True and
    False, where True indicates authorized and False, unauthorized.  Any
    attributes that are not explicitly set and, in the case of get protection,
    are not in the zope.security.checker._available_by_default list,
    will cause ForbiddenAttribute to be raised when the name is checked, as
    with the real zope.security checkers.
    """
    def __init__(self, getnames, setnames):
        self.getnames = getnames
        self.setnames = setnames
    def check_getattr(self, obj, name):
        if name not in zope.security.checker._available_by_default:
            val = self.getnames[name]
            if not val:
                raise Unauthorized
    check = check_getattr
    def check_setattr(self, obj, name):
        val = self.setnames[name]
        if not val:
            raise Unauthorized
    def proxy(self, value):
        return value

def SchemaChecker(schema, readonly=False):
    """returns a checker that allows read and write access to fields in schema.
    """
    get = {}
    set = {}
    for name, field in getFieldsInOrder(schema):
        get[name] = True
        if not field.readonly:
            if IMethod.providedBy(field):
                get[field.writer.__name__] = True
            else:
                set[name] = True
    assert not readonly
    return DummyChecker(get, set)

def securityWrap(ob, schema, readonly=False):
    return zope.security.checker.Proxy(ob, SchemaChecker(schema, readonly))
