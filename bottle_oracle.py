#! python
# -*- coding: utf-8 -*-

"""
cx_Oracle integration with Bottle framework
"""

__author__ = 'Vladimir Bormotov'
__version__ = '0.0.1'
__license__ = 'BSD'

### CUT HERE (see setup.py)

from bottle import PluginError, response
import inspect

import os
os.environ["NLS_LANG"] = ".AL32UTF8"

import cx_Oracle

class OraclePlugin(object):
    """
    Oracle Plugin for bottle
    """
    name = 'oracle'
    api = 2

    oracle_db = None

    def get_db(self):
        """return cx_Oracle Connection() instance
        """
        if self.oracle_db is None:
            self.oracle_db = cx_Oracle.connect(self.user, self.password, self.dsn)
        return self.oracle_db

    def __init__(self, uri, keyword='oradb'):
        """uri format:
        user/password@host:port:sid
        user/password@host:sid (port = '1521')
        """
        user_pass, sid = uri.split('@')
        self.user, self.password = user_pass.split('/')
        lsid = sid.split(':')
        if len(lsid) == 2:
            self.dsn = cx_Oracle.makedsn(lsid[0], 1521, lsid[1])
        elif len(lsid) == 3:
            self.dsn = cx_Oracle.makedsn(lsid[0], lsid[1], lsid[2])
        else:
            raise ValueError('URI format error: to many components in SID: ' + sid)

    def __repr__(self):
        return "<%s user='%s' password='%s' dsn='%s'>" % \
            (self.__class__.__name__, self.user, self.password, self.dsn)

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, OraclePlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError('Another copy of OraclePlugin registered with same keyword: ' + self.keyword)

    def apply(self, callback, route):
        args = inspect.getargspec(route.callback)[0]

        def wrapper(*a, **ka):
            if self.keyword in args:
                ka[self.keyword] = self.get_db()
            rv = callback(*a, **ka)
            return rv
        return wrapper

    def close(self):
        self.oracle_db.commit()
        self.oracle_db.close()
        self.oracle_db = None

Plugin = OraclePlugin

# vim: set ts=4 sts=4 sw=4 et :
