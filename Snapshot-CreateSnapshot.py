from datetime import datetime
import requests
import json
import urllib3
# Supresses the self signed cert warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLUSTERIP = '172.16.10.10'
PORT = 8080
USER = 'root'
PASS = 'a'

uri = "https://%s:%s" % (CLUSTERIP, PORT)
papi = uri + '/platform'
headers = {'Content-Type': 'application/json'}
data = json.dumps(
    {'username': USER, 'password': PASS, 'services': ['platform']})


# uri of the cluster used in the referer header
uri = f"https://{CLUSTERIP}:{PORT}"
# url of Papi used for all further calls to Papi
papi = uri + '/platform'
# Set header as content will provided in json format
headers = {'Content-Type': 'application/json'}
# Create json dictionary for auth
data = json.dumps(
    {'username': USER, 'password': PASS, 'services': ['platform']})
# create a session object to hold cookies
session = requests.Session()
# Establish session using auth credentials
response = session.post(uri + "/session/1/session",
                        data=data, headers=headers, verify=False)
if 200 <= response.status_code < 299:
    # Set headers for CSRF protection. Without these two headers all further calls with be "auth denied"
    session.headers['referer'] = uri
    session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')
    print("Authorization Successful")
else:
    print("Authorization Failed")
    print(response.content)

endpoint = '/1/snapshot/snapshots'

# Set expires for 1H
import time
t = datetime.fromtimestamp(time.time())
snapshot_path = '/ifs/data'
snapshot_duration = 3600  # 1 Hour
snapshot_name = 'papi-drive-snapshot-' + t.strftime('%H%M%S')
expires = int(time.time()) + snapshot_duration

# Take snapshot
data = json.dumps(
    {'path': snapshot_path, 'expires': expires, 'name': snapshot_name})
response = session.post(papi + endpoint, data=data,
                        headers=headers, verify=False)

if 200 <= response.status_code < 299:
    print("Snapshot Create Successful")
else:
    print("Snapshot Failed")
    print(response.content)
