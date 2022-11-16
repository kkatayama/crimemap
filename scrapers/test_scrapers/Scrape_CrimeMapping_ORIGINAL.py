#!/usr/bin/env python3
from pyproj import Transformer
from bs4 import BeautifulSoup
from rich import print
import requests
import json


x, y = -8435764.29563648, 4817706.56965843
transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
lat, lon = transformer.transform(x, y)
print(x, y)
print(lat, lon)

cookies = {
    '_ga': 'GA1.2.1804726938.1664921469',
    'ARRAffinity': 'd8e2d9c95710dcd366590b92b6d5ee116a4daafec7dc8a477c303db9979d998e',
    'ARRAffinitySameSite': 'd8e2d9c95710dcd366590b92b6d5ee116a4daafec7dc8a477c303db9979d998e',
    'TS01d49d2c': '0167437d795a79fa57aa4848fb9996b55fcf8c9c520a7c59c61b56e49ab51dd74731efd21766d35800b9efbda71dd7dd2418250433b24766aafc8dd9635520b8d631c5733ce638607f36fdc346967f7a6bc57d2248',
    '_gid': 'GA1.2.834684187.1668044824',
    'TS01c815fc': '0167437d7919fd52a139d5109ff07c93e04e4263351e711870bb46e95820c0f46f9daf9a5e9dc03b68a8cc7c23270393297ebcc996',
    '_gat': '1',
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

data = {
  'filterdata': '{"SelectedCategories":["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],"SpatialFilter":{"FilterType":0,"Filter":"{\\"x\\":-8433744.96007334,\\"y\\":4819287.336753828,\\"ad\\":\\"Newark, Delaware\\",\\"bd\\":\\"3218.69\\"}"},"TemporalFilter":{"PreviousID":3,"PreviousNumDays":7,"PreviousName":"Previous Week","FilterType":"Explicit","ExplicitStartDate":"20220901","ExplicitEndDate":"20221110"},"AgencyFilter":[]}',
  'shareMapID': '',
  'shareMapExtent': '',
  'alertID': '',
  'spatfilter': '{"rings":[[[-8437670.685750738,4816897.160447819],[-8437670.685750738,4821679.252030037],[-8429835.8903513,4821679.252030037],[-8429835.8903513,4816897.160447819],[-8437670.685750738,4816897.160447819]]],"spatialReference":{"wkid":102100,"latestWkid":3857}}'
}

response = requests.post('https://www.crimemapping.com/map/MapUpdated', headers=headers, cookies=cookies, data=data)
print(response.json())


cookies = {
    '_ga': 'GA1.2.1804726938.1664921469',
    'ARRAffinity': 'd8e2d9c95710dcd366590b92b6d5ee116a4daafec7dc8a477c303db9979d998e',
    'ARRAffinitySameSite': 'd8e2d9c95710dcd366590b92b6d5ee116a4daafec7dc8a477c303db9979d998e',
    'TS01d49d2c': '0167437d795a79fa57aa4848fb9996b55fcf8c9c520a7c59c61b56e49ab51dd74731efd21766d35800b9efbda71dd7dd2418250433b24766aafc8dd9635520b8d631c5733ce638607f36fdc346967f7a6bc57d2248',
    '_gid': 'GA1.2.834684187.1668044824',
    'TS01c815fc': '0167437d7918b67095b84a2c56866d1225c6aa83403e226a7db74c478829a2846641895cd342973b718ec2b63339fc526f2e070b98',
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

data = {
  'IDs[]': '0_28b437c8-20f1-4213-87bc-5fe7e9ebc01c',
  'x': '-8435764.29563648',
  'y': '4817706.56965843',
  'picx': '39.66726000000008',
  'picy': '-75.77976',
  'suggestNumCharacters': '3',
  'whatAttributeCategories': '[{"id":1,"na":"Arson"},{"id":2,"na":"Assault"},{"id":3,"na":"Burglary"},{"id":4,"na":"Disturbing the Peace"},{"id":5,"na":"Drugs / Alcohol Violations"},{"id":6,"na":"DUI"},{"id":7,"na":"Fraud"},{"id":8,"na":"Homicide"},{"id":9,"na":"Motor Vehicle Theft"},{"id":10,"na":"Robbery"},{"id":11,"na":"Sex Crimes"},{"id":12,"na":"Theft / Larceny"},{"id":13,"na":"Vandalism"},{"id":14,"na":"Vehicle Break-In / Theft"},{"id":15,"na":"Weapons"},{"id":17,"na":"Sex Offender"},{"id":18,"na":"Sexual Predator"}]',
  'offenderDisclaimerAccepted': 'false'
}

incident = {'x': -8432785.38606285, 'y': 4818108.60747228, 'l': 15, 'i': ['0_582ad4da-1f8b-4a17-bf5f-ae207d028f15']}
#incident = {'x': -8431356.04368974, 'y': 4820139.29026913, 'l': 4, 'i': ['0_3307fdbf-c898-4a31-ac46-55314a021460']}
#incident = {'x': -8432597.25612341, 'y': 4816076.89140114, 'l': 2, 'i': ['0_175dac8a-0cd7-4366-9dff-382306df9662']}
x, y = incident['x'], incident['y']
transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
lat, lon = transformer.transform(x, y)
print(x, y)
print(lat, lon)

data = {
  'IDs[]': incident["i"][0],
  'x': x,
  'y': y,
  'picx': lat,
  'picy': lon,
  'suggestNumCharacters': '3',
  'whatAttributeCategories': '[{"id":1,"na":"Arson"},{"id":2,"na":"Assault"},{"id":3,"na":"Burglary"},{"id":4,"na":"Disturbing the Peace"},{"id":5,"na":"Drugs / Alcohol Violations"},{"id":6,"na":"DUI"},{"id":7,"na":"Fraud"},{"id":8,"na":"Homicide"},{"id":9,"na":"Motor Vehicle Theft"},{"id":10,"na":"Robbery"},{"id":11,"na":"Sex Crimes"},{"id":12,"na":"Theft / Larceny"},{"id":13,"na":"Vandalism"},{"id":14,"na":"Vehicle Break-In / Theft"},{"id":15,"na":"Weapons"},{"id":17,"na":"Sex Offender"},{"id":18,"na":"Sexual Predator"}]',
  'offenderDisclaimerAccepted': 'false'
}

response = requests.post('https://www.crimemapping.com/map/GetDetailRecordInfo', headers=headers, cookies=cookies, data=data)
soup = BeautifulSoup(response.content, 'html5lib')
script = soup.select('script')[-1]
data = json.loads(script.string.strip().replace('var dataViewModel = ', '').split(';')[0])#["RecordList"][0]
print(data)
