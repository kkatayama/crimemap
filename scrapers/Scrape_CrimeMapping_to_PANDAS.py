# coding: utf-8
from utils import getSession, base_url
import pandas as pd


# -- fetch all entries in the incidents table
url = f'{base_url}/get/incidents'
s = getSession()
r = s.get(url)
info = r.json()
message = info.get('message')
incidents = info.get('data')

# -- print message
print(f'message: {message}')

# -- load incidents into DataFrame
df = pd.DataFrame(incidents)
df["entry_time"] = pd.to_datetime(df["entry_time"])
df["report_date"] = pd.to_datetime(df["report_date"])
print(df.head(20))
