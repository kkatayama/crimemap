#!/usr/bin/env python3
import os
for pkg in ["pyproj", "pandas", "geopy", "opencage", "bs4", "html5lib", "rich", "pick", "requests"]:
    cmd = f"import {pkg}"
    try:
        exec(cmd)
    except Exception as e:
        print(e)
        cmd = f'python3 -m pip install {pkg}'
        os.system(cmd)

from datetime import datetime
from utils.utils import getSession, base_url
from utils.crimemapping_api import CrimeMappingAPI
from rich.progress import track
from rich import print
import argparse
import sys


def init():
    """
    1. Scrape entire history of incidents reported on crimemapping.com
    2. Upload all data to the backend database
    """
    # -- log in to backed
    s = getSession()

    # -- scrape data from www.crimemapping.com
    crime = CrimeMappingAPI()
    incidents = crime.getIncidents(start_date="20220701")  # , end_date="20220703")

    # -- upload scraped data into backend
    api_url = f"{base_url}/add/incidents"
    for incident in track(incidents, 'Uploading Incidents...'):
        r = s.post(url=api_url, data=incident)
        # print(r.json())


def update():
    """
    1. Fetch the latest incident entry from the backend database
    2. Scrape succeeding incidents from crimemapping.com
    3. Upload results to backend database
    """
    # -- log in to backed
    s = getSession()

    # -- fetch the latest incident from backend
    api_url = f"{base_url}/get/incidents"
    params = {'filter': '(entry_id >= 1) ORDER BY report_date DESC LIMIT 1'}
    r = s.post(url=api_url, data=params)
    data = r.json().get('data')

    # -- scrape succeeding incidents
    start_date = datetime.strptime(data["report_date"], '%Y-%m-%d %H:%M:%S')
    crime = CrimeMappingAPI()
    incidents = crime.getIncidents(start_date=start_date.strftime('%Y%m%d'))

    # -- upload latest incidents
    api_url = f"{base_url}/add/incidents"
    for incident in track(incidents, 'Uploading Latest Incidents...'):
        report_date = datetime.strptime(incident["report_date"], '%Y-%m-%d %H:%M:%S')
        if report_date > start_date:
            r = s.post(url=api_url, data=incident)
            print(incident)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--init', required=False, action="store_true", help="scrape and upload entire history of incidents")
    ap.add_argument('--update', required=False, action="store_true", help="scrape and upload latest incidents")
    args = ap.parse_args()

    if args.init:
        init()
    if args.update:
        update()
    if not args.init and not args.update:
        print('please specify a task: --init, --update')
        print('for help, see: python3 crimemapping.py --help')


if __name__ == '__main__':
    sys.exit(main())
