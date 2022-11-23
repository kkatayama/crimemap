# -- check for required packages
from pyproj import Transformer
from bs4 import BeautifulSoup
from datetime import datetime
from rich.progress import track
from rich import print
from pick import pick
import requests
import json


LEGEND = [
    {'id': 1, 'na': 'Arson'},
    {'id': 2, 'na': 'Assault'},
    {'id': 3, 'na': 'Burglary'},
    {'id': 4, 'na': 'Disturbing the Peace'},
    {'id': 5, 'na': 'Drugs / Alcohol Violations'},
    {'id': 6, 'na': 'DUI'},
    {'id': 7, 'na': 'Fraud'},
    {'id': 8, 'na': 'Homicide'},
    {'id': 9, 'na': 'Motor Vehicle Theft'},
    {'id': 10, 'na': 'Robbery'},
    {'id': 11, 'na': 'Sex Crimes'},
    {'id': 12, 'na': 'Theft / Larceny'},
    {'id': 13, 'na': 'Vandalism'},
    {'id': 14, 'na': 'Vehicle Break-In / Theft'},
    {'id': 15, 'na': 'Weapons'},
    {'id': 17, 'na': 'Sex Offender'},
    {'id': 18, 'na': 'Sexual Predator'}
]

class CrimeMappingAPI(object):
    """Wrapper for crimemapping.com"""

    def __init__(self):
        """Constructor"""
        cookies = {
            '_ga': 'GA1.2.1804726938.1664921469',
            'ARRAffinity': 'd8e2d9c95710dcd366590b92b6d5ee116a4daafec7dc8a477c303db9979d998e',
            'ARRAffinitySameSite': 'd8e2d9c95710dcd366590b92b6d5ee116a4daafec7dc8a477c303db9979d998e',
            'TS01d49d2c': '0167437d795a79fa57aa4848fb9996b55fcf8c9c520a7c59c61b56e49ab51dd74731efd21766d35800b9efbda71dd7dd2418250433b24766aafc8dd9635520b8d631c5733ce638607f36fdc346967f7a6bc57d2248',
            '_gid': 'GA1.2.834684187.1668044824',
            'TS01c815fc': '0167437d7919fd52a139d5109ff07c93e04e4263351e711870bb46e95820c0f46f9daf9a5e9dc03b68a8cc7c23270393297ebcc996',
            # '_gat': '1',
        }

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
            'Origin': 'https://www.crimemapping.com',
            'Referer': 'https://www.crimemapping.com/map',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0 (Edition beta)',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="106", "Not.A/Brand";v="24", "Opera";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        # -- default location is Newark, DE
        location = {
            'location': 'Newark, DE, USA New Castle County',
            'id': 'dHA9MCNsb2M9Njg0MjY0MCNsbmc9NTQjcGw9MTIyNzQyMiNsYnM9MTQ6MzI3ODkxMTY7MjoxMzgxNzMwMA==',
            'iscollection': 'false',
            'maxlocations': '10'
        }

        self.s = requests.Session()
        self.s.headers.update(headers)
        self.s.cookies.update(cookies)
        self.location = location

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

    def geocodeLocation(self, location={}):
        """
        TODO: NEED TO FINISH THIS!!!

        Retrieve and convert latitude and longitude coordinates to spatial

        ARGS:
            location (:obj:`dict`, optional): georeference returned from self.searchLocation()

        RETURNS:
            spatial_refrence (json): location converted to spatial coordinates with xmax and xmin

        EXAMPLE:
            In [1]: crime = CrimeMappingAPI()
               ...: location = {
               ...:     "MagicKey": "dHA9MCNsb2M9Njg0MjY0MCNsbmc9NTQjcGw9MTIyNzQyMiNsYnM9MTQ6MzI3ODkxMTY7MjoxMzgxNzMwMA==",
               ...:     "IsCollection": 'false',
               ...:     "Text": "Newark, DE, USA (New Castle County)",
               ...:     "Source": 0
               ...: }

            In [2]: print(crime.geocodeLocation(location=location))

        """
        # -- you can force a location if you wish
        self.location = location if location else self.location
        url = 'https://www.crimemapping.com/map/GeocodeLocation'
        return self._post(url=url, data=self.location)

    
    def searchLocation(self, query='Newark, DE'):
        params = {
            'text': query,
            'x': -8435764.29563648,
            'y': 4817706.56965843,
            'filter[logic]': 'and',
            'filter[filters][0][value]': query.lower(),
            'filter[filters][0][operator]': 'startswith',
            'filter[filters][0][field]': 'Text',
            'filter[filters][0][ignoreCase]': 'true'
        }
        url = 'https://www.crimemapping.com/Map/GetLocationSuggestions'
        locations = self._get(url=url, data=params)
        if isinstance(locations, list):
            location_names = [location["Text"] for location in locations]
            name, index = pick(title='Select Location: ', options=locations, indicator='🢧')
            location = locations[index]
            self.location = {
                "location": location.get("Text"),
                "id": location.get("MagicKey"),
                "iscollection": location.get("IsCollection"),
                "maxlocations": "10"
            }
            print(f'Location: {self.location}')
            return self.geocodeLocation()

    def getMapIncidents(self, start_date="20220901", end_date=datetime.today().strftime('%Y%m%d')):
        data = {
            'filterdata': '{"SelectedCategories": ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"], "SpatialFilter": {"FilterType": 0, "Filter": "{\\"x\\": -8433744.96007334, \\"y\\": 4819287.336753828, \\"ad\\": \\"Newark, Delaware\\", \\"bd\\": \\"3218.69\\"}"}, "TemporalFilter": {"PreviousID": 3, "PreviousNumDays": 7, "PreviousName": "Previous Week", "FilterType": "Explicit", "ExplicitStartDate": "' + start_date + '", "ExplicitEndDate": "' + end_date + '"}, "AgencyFilter": []}',
            'shareMapID': '',
            'shareMapExtent': '',
            'alertID': '',
            'spatfilter': '{"rings": [[[-8437670.685750738, 4816897.160447819], [-8437670.685750738, 4821679.252030037], [-8429835.8903513, 4821679.252030037], [-8429835.8903513, 4816897.160447819], [-8437670.685750738, 4816897.160447819]]], "spatialReference": {"wkid": 102100, "latestWkid": 3857}}'
        }
        url = 'https://www.crimemapping.com/map/MapUpdated'
        return self._post(url=url, data=data)

    def getIncidentInfo(self, i='', x=0, y=0):
        transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
        lat, lon = transformer.transform(x, y)
        data = {
          'IDs[]': i,
          'x': x,
          'y': y,
          'picx': lat,
          'picy': lon,
          'suggestNumCharacters': '3',
          'whatAttributeCategories': '[{"id":1,"na":"Arson"},{"id":2,"na":"Assault"},{"id":3,"na":"Burglary"},{"id":4,"na":"Disturbing the Peace"},{"id":5,"na":"Drugs / Alcohol Violations"},{"id":6,"na":"DUI"},{"id":7,"na":"Fraud"},{"id":8,"na":"Homicide"},{"id":9,"na":"Motor Vehicle Theft"},{"id":10,"na":"Robbery"},{"id":11,"na":"Sex Crimes"},{"id":12,"na":"Theft / Larceny"},{"id":13,"na":"Vandalism"},{"id":14,"na":"Vehicle Break-In / Theft"},{"id":15,"na":"Weapons"},{"id":17,"na":"Sex Offender"},{"id":18,"na":"Sexual Predator"}]',
          'offenderDisclaimerAccepted': 'true'
        }
        url = 'https://www.crimemapping.com/map/GetDetailRecordInfo'
        r = self._post(url=url, data=data)
        soup = BeautifulSoup(r, 'html5lib')
        # print(soup.prettify())
        script = soup.select('script')[-1]
        info_all = json.loads(script.string.strip().replace('var dataViewModel = ', '').split(';')[0])
        info_type = LEGEND[int(info_all['LegendID'])]
        info_date = str(datetime.strptime(info_all["CrimeReportDate"], '%m-%d-%Y @ %I:%M %p'))

        tier = 1
        incident_id = info_all["CrimeCaseNumber"] if info_all.get("CrimeCaseNumber") else 1
        description = info_all["CrimeDescription"] if info_all.get("CrimeDescription") else info_type["na"]
        location = info_all["Address"] if info_all.get("Address") else "NO ADDRESS"
        latitude = lat,
        longitude = lon,
        agency = info_all['OrganizationName'] if info_all.get('OrganizationName') else "UNKNOWN POLICE"
        report_date = info_date

        info = {
            'tier': tier,
            'type': info_type["na"],
            'type_img': f'{info_type["id"]}.svg',
            'description': description,
            'location': location,
            'latitude': latitude,
            'longitude': longitude,
            'agency': agency,
            'report_date': report_date,
        }
        return info

    def getIncidents(self, start_date="20220901", end_date=datetime.today().strftime('%Y%m%d')):
        map_incidents = self.getMapIncidents(start_date=start_date, end_date=end_date)
        incidents = []
        for incident in track(map_incidents["result"]["rs"], "Processing Incidents..."):
            for i in incident["i"]:
                incidents.append(self.getIncidentInfo(i=i, x=incident['x'], y=incident['y']))
        return sorted(incidents, key=lambda k: k["report_date"])
