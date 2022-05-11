CLUSTERIP = '172.16.10.10'
PORT = 8080
USER = 'root'
PASS = 'a'

import requests
import json
import urllib3
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning)  # Supresses the self signed cert warning
# uri of the cluster used in the referer header
uri = f"https://{CLUSTERIP}:{PORT}"
# url of Papi used for all further calls to Papi
papi = f'{uri}/platform'
# Set header as content will provided in json format
headers = {'Content-Type': 'application/json'}
# Create json dictionary for auth
data = json.dumps({'username': USER, 'password': PASS, 'services': ['platform']})
# create a session object to hold cookies
session = requests.Session()
# Establish session using auth credentials
response = session.post(f"{uri}/session/1/session", data=data, headers=headers, verify=False)

if 200 <= response.status_code < 299:
    # Set headers for CSRF protection. Without these two headers all further calls with be "auth denied"
    session.headers['referer'] = uri
    session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')
    print("Authorization Successful")
else:
    print("Authorization Failed")
    print(response.content)

response = session.get(papi + '/3/cluster/config', verify=False)
if 200 <= response.status_code < 299:
    print(response.json())
else:
    print(f"Error: {response.content}")
