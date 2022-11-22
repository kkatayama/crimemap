#!/usr/bin/env python3

from datetime import datetime
from rich.progress import track
from rich import print
import requests


class SexOffenderAPI(object):
    """Wrapper for sexoffender.dsp.delaware.gov"""

    def __init__(self):
        """Constructor"""

        cookies = {
            '__RequestVerificationToken': 'AfPHuMdVOuUOlQSiFj-LxvvyCVpVniOAP4U5dN77o144W973eAf73ZeeVmmFIaukpp2gl77ajkX12dR4FFoZphazbbvpr3tdeRlWMVwkEHA1',
            '_ga': 'GA1.2.1070525134.1668047881',
            '_gid': 'GA1.2.1599056964.1668739761',
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
            'Origin': 'https://sexoffender.dsp.delaware.gov',
            'Referer': 'https://sexoffender.dsp.delaware.gov/?/Search/SearchType/neighborhood/XLongitudeMin/-75.8040226211533/XLongitudeMax/-75.70617563629014/YLatitudeMin/39.65765407962261/YLatitudeMax/39.69728986493103',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition beta)',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        self.s = requests.Session()
        self.s.headers.update(headers)
        self.s.cookies.update(cookies)
        self.api_url = 'https://sexoffender.dsp.delaware.gov'


    def _get(self, url='', data=''):
        """Wrapper for requests.Session().get()"""
        r = self.s.get(url=url, params=data)
        return self._response(r=r)

    def _post(self, url='', data=''):
        """Wrapper for requests.Session().post()"""
        r = self.s.post(url=url, data=data)
        return self._response(r=r)

    def _response(self, r=requests.Response()):
        """Function to return JSON response"""
        try:
            return r.json()
        except Exception:
            return r.text

    def clean(self, obj={}, keys=[]):
        line = ""
        for key in keys:
            if obj[key]:
                line += str(obj[key]) + " "
        return line.strip()

    def getOffenders(self):
        data = {
            'SearchType': 'neighborhood',
            'LastName': '',
            'FirstName': '',
            'HouseNumber': '',
            'StreetPrefix': '',
            'StreetName': '',
            'StreetType': '',
            'Development': '',
            'County': '',
            'City': '',
            'ZipCode': '',
            'XLongitudeMin': '-75.8040226211533',
            'XLongitudeMax': '-75.70617563629014',
            'YLatitudeMin': '39.65765407962261',
            'YLatitudeMax': '39.69728986493103',
            'ExcludeInJail': 'false',
            'IncludeHomeless': 'false',
            'IncludeWanted': 'false',
            'Workplace': '',
            'ConvictionState': '',
            'OnlineId': '',
            'PageSize': '8',
            '__RequestVerificationToken': 'oiFFttCg4Bey-nbnwjY4esqghj9pmO9pDiigm0mXAiU6xIG3lvVSf7g4XfdsgzYGYa_WR-tRT1UDOA6y57eccs8akgePqJdSLNp2RgU_5YM1'
        }
        url = f'{self.api_url}/Search'
        url = 'https://sexoffender.dsp.delaware.gov/Search'
        results = self._post(url=url, data=data)["offenders"]

        offenders = []
        for info in results:
            try:
                offender = {
                    "tier": self.clean(info, ["RiskLevel"]),
                    "name": self.clean(info["Name"], ["FirstName", "LastName"]),
                    "dob": str(datetime.strptime(info["DateOfBirth"], "%Y-%m-%dT%H:%M:%S")),
                    "arrest_description": self.clean(info["Arrests"][0], ["Description"]),
                    "arrest_date": str(datetime.strptime(info["Arrests"][0]["AdjudicationDate"], "%Y-%m-%dT%H:%M:%S")),
                    "victim_age": self.clean(info["Arrests"][0], ["VictimAge"]),
                    "home_address": self.clean(info["HomeAddress"], keys=["StreetNumber", "StreetPrefix", "StreetName", "StreetType"]),
                    "home_latitude": self.clean(info["HomeAddress"], keys=["YLatitude"]),
                    "home_longitude": self.clean(info["HomeAddress"], keys=["XLongitude"]),
                    "work_name": self.clean(info["WorkAddress"], keys=["Comments"]),
                    "work_address": self.clean(info["WorkAddress"], ["StreetNumber", "StreetPrefix", "StreetName", "StreetType"]),
                    "work_latitude": self.clean(info["WorkAddress"], keys=["YLatitude"]),
                    "work_longitude": self.clean(info["WorkAddress"], keys=["XLongitude"]),
                }
                offenders.append(offender)
            except:
                pass
        return offenders
