#! python

import sys
import bottle
from bottle_oracle import OraclePlugin

USER = 'sys'
PASS = 'oracle'
HOST = 'db'
SID = 'demo'

URI = '%s/%s@%s:%s as sysdba' % (USER, PASS, HOST, SID)

Q_FIELDS = ['sid', 'username', 'serial#', 'status', 'schemaname', 'machine', 'module']
Q_SESSIONS = """select %s
 from v$session
 where upper(username) = upper('%%s')
 order by status, sid
""" % ','.join(Q_FIELDS)

app = bottle.Bottle()

@app.get("/")
def index_page(oradb):
    rows = oradb.cursor().execute(Q_SESSIONS % plugin.user).fetchall()
    return bottle.template('index', sessions=rows, user=plugin.user, fields=Q_FIELDS)


if len(sys.argv) > 1:
    uri = sys.argv[1]
    print "used uri:", uri
    plugin = OraclePlugin(uri)
else:
    print 'default uri:', URI
    plugin = OraclePlugin(URI)

app.install(plugin)

app.run(host="0.0.0.0", port=8082, reloader=True)

# vim: set ts=4 sts=4 sw=4 et :
