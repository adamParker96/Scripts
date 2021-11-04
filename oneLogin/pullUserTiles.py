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

file = open('FILENAMEHERE.csv', "rU")
reader = csv.reader(file, delimiter=',')
row_count = sum(1 for row in reader)
file.close()
print(str(row_count) + ' users to check')

file = open('FILENAMEHERE.csv', "rU")
reader = csv.reader(file, delimiter=',')

for row2 in reader:
    userID = str(row2[5]) ##OR WHATEVER COLUMN USERID IS IN
    userEmail = str(row2[1]) ##SAME FOR USER EMAIL
    try:
        userApps = requests.get(
            url='https://api.us.onelogin.com/api/1/users/' + userID + '/apps',
            data=json.dumps({
                "status": 0
            }),
            headers={
                "Authorization": "bearer:" + oAuth,
            },
        ).json()
        x = len(userApps['data'])
        y = 0
        myApps = ''
        print('retrieved information for ' + str(userEmail))
        #while y < x):  ## only uncomment if you need the name of the apps
        #    myApps = myApps + userApps['data'][x]['name'] + '\t'
        #    y += 1
        with open('pullEmployeeApps' + str(todayDate) + '.tsv','a') as myFile2:  ## add the headers to the CSV  #only include this section if this is your first time running the script
            myFile2.writelines(userEmail + ', ' + str(x) + '\n')
    except:
        print ('couldnt pull information for this user. skipping')
print('done')
