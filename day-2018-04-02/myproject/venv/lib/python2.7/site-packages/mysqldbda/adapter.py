##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""MySQL database adapter.

$Id: Adapter.py,v 1.1 2004/10/10 mriya3
"""

import sys

from zope.interface import directlyProvides
from zope.rdb.interfaces import IZopeConnection
from zope.rdb import ZopeDatabaseAdapter, parseDSN
from zope.publisher.interfaces import Retry

import MySQLdb


class IMySQLZopeConnection(IZopeConnection):
    """A marker interface stating that this connection uses the MySQL SQL."""


class MySQLStringConverter:

    def __init__(self, encoding):
        self.encoding = encoding

    def __call__(self, string):
        if isinstance(string, str):
            return string.decode(self.encoding)
        return string

class MySQLdbAdapter(ZopeDatabaseAdapter):
    """A MySQLdb adapter for Zope3"""

    # MySQLdb types codes
    __STRINGtypes = (1, 247, 254, 253)
    __BINARYtypes = (252, 251, 250, 249)
    __DATEtypes = (10, 14)
    __DATETIMEtypes = (7, 12)
    __NUMBERtypes = (0, 5, 4, 9, 3, 8, 1, 13)
    __TIMEtypes = (11)

    def __init__(self, *args, **kw):
        super(MySQLdbAdapter, self).__init__(*args, **kw)
        # Default string converter
        self.__stringConverter =  MySQLStringConverter(self.getEncoding())

    def _connection_factory(self):
        """Create a MySQLdb DBI connection based on the DSN"""

        conn_info = parseDSN(self.dsn)

        connection = MySQLdb.Connect(db=conn_info['dbname'],
                            host=conn_info['host'],
                            user=conn_info['username'],
                            passwd=conn_info['password'],
                            port=int(conn_info['port'] or '3306'))

        if self.__stringConverter.encoding != self.getEncoding():
            #avoid resetting this everytime, otherwise the adapter
            #gets modified on each connection and that causes ZODB conflicts
            self.__stringConverter = MySQLStringConverter(self.getEncoding())
        return connection

    def getConverter(self, type):
        'See IDBITypeInfo'
        if type in self.__STRINGtypes:
            return self.__stringConverter
        return self.identity

    def identity(self, x):
        return x

    def setEncoding(self, encoding):
        super(MySQLdbAdapter, self).setEncoding(encoding)
        self.__stringConverter = MySQLStringConverter(self.getEncoding())

    def __call__(self):
        connection = ZopeDatabaseAdapter.__call__(self)
        directlyProvides(connection, IMySQLZopeConnection)
        return connection

    def isConnected(self):
        """Check if we are connected to a database.

        Try to solve the dissapearing connection problem. For background, see
        http://mail.zope.org/pipermail/zope3-dev/2005-December/017052.html
        """
        if self._v_connection is None:
            return False
        try:
            # Note, this might automatically re-connect to the DB
            # but then again might not... I've seen both.
            self._v_connection.ping()
        except MySQLdb.OperationalError:
            retry = Retry(sys.exc_info())
            try:
                # this is a bare except because at this point
                # we are just trying to be nice closing the connection.
                self._v_connection.close()
            except:
                pass
            self._v_connection = None
            # raise a retry exception and let the publisher try again
            raise retry
        return True
