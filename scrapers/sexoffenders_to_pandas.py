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
url = f'{base_url}/get/sex_offenders'
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
df["arrest_date"] = pd.to_datetime(df["arrest_date"])
df["dob"] = pd.to_datetime(df["dob"])

# -- since each row contains alot of information, let's split the output
print("=== ARREST INFO ===")
print(df[["tier", "name", "dob", "arrest_description", "arrest_date", "victim_age"]].head(10))

print("=== ADDRESS INFO ===")
print(df[["tier", "name", "home_address", "home_latitude", "home_longitude", "work_name", "work_address", "work_latitude", "work_longitude"]].head(10))
