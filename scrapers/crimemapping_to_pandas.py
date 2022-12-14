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
from rich import print
import pandas as pd


# -- log in to backend
s = getSession()

# -- fetch all entries in the incidents table
url = f'{base_url}/get/incidents'
r = s.get(url)
info = r.json()
message = info.get('message')
incidents = info.get('data')
print(url, '\n')

# -- print message
print(f'message: {message}', '\n')

# -- load incidents into DataFrame
df = pd.DataFrame(incidents)
df["entry_time"] = pd.to_datetime(df["entry_time"])
df["report_date"] = pd.to_datetime(df["report_date"])
print('=== FIRST 10 INCIDENTS ===')
print(df.sort_values(by='report_date', ascending=True).head(10))

print('=== LATEST 10 INCIDENTS ===')
print(df.sort_values(by='report_date', ascending=False).head(10))
