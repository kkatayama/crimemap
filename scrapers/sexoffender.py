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

from utils.utils import getSession, base_url
from utils.sexoffender_api import SexOffenderAPI
from rich.progress import track
from rich import print
import argparse
import sys


def init():
    """
    1. Scrape entire history of sex offenders reported on sexoffender.dsp.delaware.gov
    2. Upload all data to the backend database
    """
    # -- log in to backed
    s = getSession()

    # -- scrape data from www.crimemapping.com
    api = SexOffenderAPI()
    offenders = api.getOffenders()

    # -- upload scraped data into backend
    api_url = f"{base_url}/add/sex_offenders"
    for offender in track(offenders, 'Uploading Sex Offenders...'):
        r = s.post(url=api_url, data=offender)
        # print(r.json())


def update():
    """
    1. Fetch the latest sex offender entry from the backend database
    2. Scrape succeeding sex offenders from sexoffender.dsp.delaware.gov
    3. Upload results to backend database
    """
    # -- log in to backed
    s = getSession()

    # -- fetch the latest incident from backend
    api_url = f"{base_url}/get/sex_offenders"
    ### TODO: FINISH THIS... ###


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--init', required=False, action="store_true", help="scrape and upload entire history of sex offenders")
    ap.add_argument('--update', required=False, action="store_true", help="NOT FINISHED YET...")
    args = ap.parse_args()

    if args.init:
        init()
    if args.update:
        update()
    if not args.init and not args.update:
        print('please specify a task: --init, --update')
        print('for help, see: python3 sexoffender.py --help')


if __name__ == '__main__':
    sys.exit(main())
