#!/usr/bin/python

import cgi
import psycopg2 as pg
from psycopg2 import sql

DB_NAME='austin_data'
DB_USER='postgres'
DB_PASS='postgres'

#Get HTTP parameters.
ARGS = cgi.FieldStorage()

args = {}

if 'crime_type' in ARGS:
    args['crime_type'] = ARGS['crime_type'].value
else:
    args['crime_type'] = ''

if 'begin_date' in ARGS:
    args['begin_date'] = ARGS['begin_date'].value
else:
    args['begin_date'] = '2016-01-01'

if 'end_date' in ARGS:
    args['end_date'] = ARGS['end_date'].value
else:
    args['end_date'] = '2016-12-31'

#Open the connection.
conn = pg.connect('dbname={0} user={1} password={2}'.format(DB_NAME, DB_USER, DB_PASS))

#Open a cursor.
cur = conn.cursor()


#Read query files.
web_path = '/home/jorge/web/incident_extract/'

query1 = open(web_path + 'column_names.sql', 'r').read()

query2 = open(web_path + 'crime_types.sql', 'r').read()

query3 = sql.SQL( open(web_path + 'table_data.sql', 'r').read() ).format(sql.Literal(args['crime_type']), sql.Literal(args['begin_date']), sql.Literal(args['end_date']))


#Execute and fetch result-sets.
cur.execute(query1)
headers = cur.fetchall()

cur.execute(query2)
params = cur.fetchall()

cur.execute(query3)
results = cur.fetchall()


#Print HTML headers and content.
print 'Content-Type: text/html\n'


crime_types = ''
table_headers = ''
table_data = ''


for param in params:
    val = param[0]
    crime_types += '<option value="{0}" {1}>{0}</option>\n'.format(val, 'selected="selected"' if args['crime_type']==val else '')


for hdr in headers:
    table_headers += '<th class="'+str(hdr[0])+'">'+str(hdr[0])+'</th>\n' 

for row in results:
    table_data += '<tr>\n'
    for col in row:
        table_data += '<td> ' +str(col)+ ' </td>\n'
    table_data += '</tr>\n'


page_body = open(web_path + 'index.html', 'r').read()

tokens = [
    ('{{crime_types}}', crime_types),
    ('{{table_headers}}', table_headers),
    ('{{table_data}}', table_data),
    ('{{begin_date}}', args['begin_date']),
    ('{{end_date}}', args['end_date'])
]

for token in tokens:
    page_body = page_body.replace(token[0], token[1])

#page_body = page_body.replace('{{crime_types}}', crime_types)
#page_body = page_body.replace('{{table_headers}}', table_headers)
#page_body = page_body.replace('{{table_data}}', table_data)

print page_body


#Commit transactions and clean up.
conn.commit()

cur.close()
conn.close()
