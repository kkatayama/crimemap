#!/usr/bin/env python3
from pathlib import Path
import sys
from utils import get_py_path
import argparse
import random
import query
import time
import re


def register(users=False):
    if users:
        # -- register 6 users
        for user in ['alice', 'bob', 'anna', 'steve']:
            q = f'/register/username/{user}/password/{user}/password2/{user}'
            print('---')
            query.executeQuery(base_url=base_url, query=q)
        print('---')

def delete(users=False):
    if users:
        # -- delete 6 users
        for user in ['alice', 'bob', 'anna', 'steve']:
            q = f'/delete/users/username/{user}'
            print('---')
            query.executeQuery(base_url=base_url, query=q)
        print('---')

def examine():
    table_names = [t['name'] for t in query.executeQuery(base_url=base_url, query='/get', stdout=False)["tables"]]
    for name in table_names:
        print(f'#### `{name}` table:')
        query.executeQuery(base_url=base_url, query=f'/get/{name}', short=False)

def deleteTables():
    table_names = [t['name'] for t in query.executeQuery(base_url=base_url, query='/get', stdout=False)["tables"]]
    for name in table_names:
        if name not in ['users', 'cards', 'deck']:
            print(f'#### `{name}` table:')
            query.executeQuery(base_url=base_url, query=f'/deleteTable/{name}', short=False)

def createTables():
    for name in ["user_profiles", "incidents", "sex_offenders"]:
        q = f'/createTable/{name}'
        if name == "user_profiles":
            q += '/entry_id/INTEGER/user_id/INTEGER/name/TEXT/email/TEXT/profile_pic/TEXT/entry_time/DATETIME'
        if name == "incidents":
            q += '/entry_id/INTEGER/tier/INTEGER/type/TEXT/type_img/TEXT/description/TEXT/location/TEXT/latitude/DOUBLE/longitude/DOUBLE/agency/TEXT/report_date/DATETIME/entry_time/DATETIME'
        if name == "sex_offenders":
            q += '/entry_id/INTEGER/tier/INTEGER/name/TEXT/dob/DATETIME/arrest_description/TEXT/arrest_date/DATETIME/victim_age/TEXT/home_address/TEXT/home_latitude/DOUBLE/home_longitude/DOUBLE/work_name/TEXT/work_address/TEXT/work_latitude/DOUBLE/work_longitude/DOUBLE/entry_time/DATETIME'
        query.executeQuery(base_url=base_url, query=q, short=True)

def printTables():
    print('\n<table>\n')
    for table in query.executeQuery(base_url=base_url, query='/get', stdout=False)["tables"]:
        name = table["name"]
        cols = [t["name"] for t in table["columns"]]
        print('<tr><td> Table Name </td><td> Column Names </td></tr>')
        print(f'<tr><td>\n\n```rexx\n{name}\n```\n\n</td><td>\n\n```jq\n{cols}\n```\n\n</td></tr>'.replace("'", '"'))
    print('</table>')

def uploadPics():
    for i in range(1, 19):
        url = f'https://ocpd-content.azureedge.net/cdn/images/IncidentType/Identify/{i}.svg'
        q = f'/uploadImageUrl?url={url}'
        query.executeQuery(base_url=base_url, query=q, short=True)

if __name__ == '__main__':
    domain = re.search(r'[a-z]+', get_py_path().parent.name).group().replace('bartend', 'bartender')
    base_url = f'https://{domain}.hopto.org'

    ap = argparse.ArgumentParser()
    ap.add_argument('--register', default=False, action="store_true", help="call /register")
    ap.add_argument('--delete', default=False, action="store_true", help="call /delete")
    ap.add_argument('--examine', default=False, action="store_true", help="call /get")
    ap.add_argument('--users', required=False, action="store_true", help="table to perform action on")
    ap.add_argument('--createTables', required=False, action="store_true", help='call /createTables')
    ap.add_argument('--deleteTables', required=False, action="store_true", help='call /deleteTables')
    ap.add_argument('--printTables', required=False, action="store_true", help='call /printTables')
    ap.add_argument('--uploadPics', required=False, action="store_true", help='call /uploadPics')
    args = ap.parse_args()

    if args.register:
        register(users=args.users)
    if args.delete:
        delete(users=args.users)
    if args.examine:
        examine()
    if args.createTables:
        createTables()
    if args.deleteTables:
        deleteTables()
    if args.uploadPics:
        uploadPics()
    if args.printTables:
        printTables()
