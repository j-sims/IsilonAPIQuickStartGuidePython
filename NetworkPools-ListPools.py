import requests
import json
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Suppresses the self signed cert warning

   
CLUSTERIP = '172.16.10.10'
PORT = 8080
USER = 'root'
PASS = 'a'

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning)  # Supresses the self signed cert warning

uri = f"https://{CLUSTERIP}:{PORT}"
papi = f'{uri}/platform'
headers = {'Content-Type': 'application/json'}
data = json.dumps({'username': USER, 'password': PASS, 'services': ['platform']})
session = requests.Session()
response = session.post(
    f"{uri}/session/1/session", data=data, headers=headers, verify=False)
session.headers['referer'] = uri
session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')

endpoint = '/3/network/pools'

response = session.get(papi + endpoint, verify=False)


if 200 <= response.status_code < 299:
    print("Snapshot Create Successful")
else:
    print("Snapshot Failed")
    print(response.content)


for pool in response.json()['pools']:
    print(f"{pool['name']}")

