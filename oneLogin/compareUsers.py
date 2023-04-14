import requests
import csv
import json
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
print(oAuth)
url = "https://api.us.onelogin.com/api/1/users/"
file = open('LIST_OF_USERS.csv', "rU") ##list of users from whatever system you're comparing against OL
reader = csv.reader(file, delimiter=',')
for row in reader:
    userProfile = requests.get(
            url= url + '?email=' + str(row[0]), ##assuming email is in the first column of each row
            data=json.dumps({
                "status": 0
            }),
            headers={
                "Authorization": "bearer:" + oAuth,
            },
    ).json()
    print(userProfile['data'])
    try:
        status = userProfile['data'][0]['status']
        title = userProfile['data'][0]['title']
        email = userProfile['data'][0]['email']
        print(status)
        print(title)
        if str(status) == '2':
            print('WOOHOO')
            with open('jiraAuditOutput.csv', 'a') as myFile:  # write our new line to a file, then advance
                myFile.writelines(email + ',' + title + ',' + str(status) + '\n')
        else:
            continue
    except:
        print('bad profile')
        with open('jiraAuditOutput.csv', 'a') as myFile:  # write our new line to a file, then advance
            ##myFile.writelines(email + ',' + title + ',' + str(status) + '\n')
            myFile.writelines(row[0] + ' profile errored out when we tried to look at it' + '\n')
print('done :)')
