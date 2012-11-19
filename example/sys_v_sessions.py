#! python

import bottle
import cx_Oracle
from bottle_oracle import OraclePlugin

USER = 'sys'
PASS = 'oracle'
HOST = 'db'
SID = 'demo'

URI = '%s/%s@%s:%s as sysdba' % (USER, PASS, HOST, SID)

app = bottle.Bottle()
plugin = OraclePlugin(URI)
app.install(plugin)

Q_FIELDS = ['sid', 'username', 'serial#', 'status', 'schemaname', 'machine', 'module']
Q_SESSIONS = """select %s
 from v$session
 where upper(username) = upper('%%s')
 order by status, sid
""" % ','.join(Q_FIELDS)

@app.get("/")
def index_page(oradb):
    rows = cx_Oracle.Cursor(oradb).execute(Q_SESSIONS % plugin.user).fetchall()
    return bottle.template('index', sessions=rows, user=plugin.user, fields=Q_FIELDS)

app.run(host="0.0.0.0", port=8082, reloader=True)
