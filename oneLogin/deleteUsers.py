import requests
import json
import csv
oneLoginAuth = "client_id : CLIENT_ID, client_secret : CLIENT_SECRET"
r = requests.post(
            url="https://api.us.onelogin.com/auth/oauth2/v2/token",
            headers={
                "Content-Type": "application/json",
                "Authorization": oneLoginAuth,  # change this to swap between sandbox and prod
            },
            data=json.dumps({
                "grant_type": "client_credentials"
            })
        )
try:
    if (r.json()['status']['error'] == 'true'):
        print(r.json())
except:
    print('Auth Token Generated')
oAuth = r.json()['access_token']

file = open('PATH_TO_FILE_GOES_HERE', "rU") ## location of your user CSV
reader = csv.reader(file, delimiter=',')

for row in reader:
    OLID = str(row[0])
    try:
        deleteUser = requests.delete(
            url='https://api.us.onelogin.com/api/2/users/' + OLID,
            headers={
                "Authorization": "bearer:" + oAuth,
                "Content-Type": "application/json"
            },
        ).json()
    except:
        print('error deleting user ' + OLID)
