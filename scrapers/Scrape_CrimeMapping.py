#!/usr/bin/env python3
from crimemapping_api import CrimeMappingAPI
from rich.progress import track
from rich import print
from utils import getSession, base_url


# -- log in to backed
s = getSession()

# -- scrape data from www.crimemapping.com
crime = CrimeMappingAPI()
incidents = crime.getIncidents(start_date="20220701")  # , end_date="20220703")

# -- upload scraped data into backend
for incident in track(incidents, 'Uploading Incidents...'):
    incident.update({"tier": 1})
    r = s.post(url=f"{base_url}/add/incidents", data=incident)
    # print(r.json())
