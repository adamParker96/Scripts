import requests
import json
from datetime import datetime
import csv
todayDate = datetime.today().strftime('%m-%d-%Y')
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'

r = requests.post(
            url="https://api.us.onelogin.com/auth/oauth2/v2/token",
            headers={
                "Content-Type": "application/json",
                "Authorization": "client_id : " + client_id + ',' + 'client_secret : ' + client_secret,
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
file = open('CSV_FILE_GOES_HERE', "rU") ## location of your user CSV
reader = csv.reader(file, delimiter=',')
counter = 0
row_count = NUMBER_OF_ROWS_IN_CSV_GOES_HERE
for row in reader:
    print('---------------------------------------')
    email = str(row[0])  ##assuming emails are the first column in your CSV
    if counter < row_count:
        print(row[0])
        try:
            getProfile = requests.get(
                url='https://api.us.onelogin.com/api/1/users?email=' + email,
                params={
                },
                headers={
                    "Authorization": "bearer:" + oAuth,
                    "Content-Type": "application/json"
                },
            ).json()

            ##print(getProfile)
            try:
                userID = str(getProfile['data'][0]['id'])
                userProfile = requests.put(
                    url='https://api.us.onelogin.com/api/1/users/' + userID + '/remove_roles',
                    headers={
                        "Authorization": "bearer:" + oAuth,
                        "Content-Type": "application/json"
                    },
                    data=json.dumps({
                        "role_id_array": [
                            role_id_goes_here  ##change the id (int) depending on the role(s) you want to remove
                        ]
                    })
                ).json()
                ##print(userProfile)
                print(email + ' successfully updated')
                counter += 1
                percentDone = str(int((counter / row_count) * 100))
                print(percentDone + '% complete')
            except:
                print('couldnt get ' + email + '\'s ID, skipping')
                with open('failedUsers' + todayDate + '.csv', 'a') as myFile:  # write our new line to a file, then advance
                    myFile.writelines(email + '\n')
                continue
        except:
            print("something broke when trying to extract information from " + email +"'s account")
            with open('failedUsers' + todayDate + '.csv', 'a') as myFile:  # write our new line to a file, then advance
                myFile.writelines(email + '\n')
    else:
        break
print('done')
