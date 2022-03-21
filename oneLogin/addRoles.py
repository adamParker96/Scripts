##used for bulk adding users to a certain role(s)

import requests
import json
from datetime import datetime
import csv

todayDate = datetime.today().strftime('%m-%d-%Y')
oneLoginAuth = "client_id : CLIENT_ID_GOES_HERE, client_secret : CLIENT_SECRET_GOES_HERE"
r = requests.post(
            url="https://api.us.onelogin.com/auth/oauth2/v2/token",
            headers={
                "Content-Type": "application/json",
                "Authorization": oneLoginAuth,  
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

file = open('LIST_OF_USERS_GOES_HERE.csv', "rU")
reader = csv.reader(file, delimiter=',')
counter = 0
row_count = sum(1 for row in reader)
file.close()
print(str(row_count) + ' users to add')

file = open('LIST_OF_USERS_GOES_HERE.csv', "rU")
reader = csv.reader(file, delimiter=',')
for row in reader:
    print('---------------------------------------')
    if counter < row_count:
        email = str(row[1]) ##or whatever column # email is in
        getProfile = requests.get(
            url='https://api.us.onelogin.com/api/1/users?email=' + email,
            params={
            },
            headers={
                "Authorization": "bearer:" + oAuth,
                "Content-Type": "application/json"
            },
        ).json()
        print(getProfile)
        try:
            userID = str(getProfile['data'][0]['id'])
        except:
            print('couldnt get ' + email + '\'s ID, skipping')
            continue
        userProfile = requests.put(
            url= 'https://api.us.onelogin.com/api/1/users/' + userID + '/add_roles',
            headers={
                "Authorization": "bearer:" + oAuth,
                "Content-Type" : "application/json"
            },
            data=json.dumps({
                "role_id_array":[
                    11111          ##change the id depending on the role, must be an int 
                ]
            })
        ).json()
        print(email + ' successfully updated')
        counter += 1
    else:
        break
print('done')
