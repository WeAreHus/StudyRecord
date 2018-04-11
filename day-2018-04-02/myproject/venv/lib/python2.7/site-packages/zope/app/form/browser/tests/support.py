##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""General test support.

$Id$
"""
import re
from zope.configuration import xmlconfig
from zope.formlib.tests.support import (VerifyResults,
                                        patternExists)

def registerEditForm(schema, widgets=()):
    """Registers an edit form for the specified schema.

    widgets is a mapping of field name to dict. The dict for each field must
    contain a 'class' item, which is the widget class, and any additional
    widget attributes (e.g. text field size, rows, cols, etc.)
    """
    widgetsXml = []
    for field in widgets: # pragma: no cover
        widgetsXml.append('<widget field="%s"' % field)
        for attr in widgets[field]:
            widgetsXml.append(' %s="%s"' % (attr, widgets[field][attr]))
        widgetsXml.append(' />')
    xmlconfig.string("""
        <configure xmlns="http://namespaces.zope.org/browser">
          <include package="zope.app.form.browser" file="meta.zcml" />
          <editform
            name="edit.html"
            schema="%s"
            permission="zope.View">
            %s
          </editform>
        </configure>
        """ % (schema.__identifier__, ''.join(widgetsXml)))


def defineSecurity(class_, schema):
    class_ = '%s.%s' % (class_.__module__, class_.__name__)
    schema = schema.__identifier__
    xmlconfig.string("""
        <configure xmlns="http://namespaces.zope.org/zope">
          <include package="zope.security" file="meta.zcml" />
          <class class="%s">
            <require
              permission="zope.Public"
              interface="%s"
              set_schema="%s" />
          </class>
        </configure>
        """ % (class_, schema, schema))
