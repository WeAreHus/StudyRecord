##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""zope.app.form common test related classes/functions/objects.

$Id$
"""

__docformat__ = "reStructuredText"

import os
import zope.interface
import zope.component
from zope.publisher.browser import IBrowserRequest
from zope.publisher.interfaces import IDefaultViewName
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.traversing.interfaces import ITraversable

import zope.app.form
import zope.app.wsgi.testlayer

AppFormLayer = zope.app.wsgi.testlayer.BrowserLayer(zope.app.form)

def browserView(for_, name, factory, layer=IDefaultBrowserLayer,
                providing=zope.interface.Interface):
    """Define a global browser view
    """
    provideAdapter(for_, providing, factory, name, (layer,))

def browserViewProviding(for_, factory, providing, layer=IDefaultBrowserLayer):
    """Define a view providing a particular interface."""
    return browserView(for_, '', factory, layer, providing)


stypes = list, tuple
def provideAdapter(required, provided, factory, name='', using=None, **kw):
    assert 'with' not in kw
    assert not isinstance(factory, stypes), "Factory cannot be a list or tuple"

    gsm = zope.component.getGlobalSiteManager()

    if using:
        required = (required, ) + tuple(using)
    elif not isinstance(required, stypes):
        required = (required,)

    gsm.registerAdapter(factory, required, provided, name, event=False)

def provideUtility(provided, component, name=''):
    gsm = zope.component.getGlobalSiteManager()
    gsm.registerUtility(component, provided, name, event=False)
