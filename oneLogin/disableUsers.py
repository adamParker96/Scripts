import requests
import json
import csv
from datetime import datetime
from datetime import timedelta
import random
client_id = 'CLIENT_ID' ##client ID
client_secret = 'CLIENT_SECRET' ##client Secret

r = requests.post( ##get our OAUTH token
			url="https://DOMAIN.onelogin.com/auth/oauth2/v2/token",
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
print('oauth token: ' + oAuth)
##take a CSV of all our users in OL (this is much faster than pulling the users via API)
file = open('FILE_NAME.csv', encoding='utf8') ## location of your user CSV
reader = csv.reader(file, delimiter=',')
##then we iterate through the users
for row in reader:
	print('---------------------------------------')
	email = str(row[0])  ##assuming emails are the first column in your CSV
	print(email)
	try:
		getUser = requests.get( ##for each user, update their password first
			url="https://DOMAIN.onelogin.com/api/2/users/?email=" + email,
			headers={
				"Authorization": "Bearer " + oAuth,
				"Content-Type": "application/json"
			}
		).json()
		print(getUser)
		userID = str(getUser[0]['id'])
		print(userID)
	except:
		print('Something broke while pulling ' + email + '\'s user ID')
	try:
		disableUser = requests.put( ##for each user, update their password first
			url='https://DOMAIN.onelogin.com/api/2/users/' + userID,
			headers={
				"Authorization": "Bearer " + oAuth,
				"Content-Type": "application/json"
			},
			data=json.dumps({
				"state": 3,  ##change the state (3 is unlicensed)
				"status": 2 ##change the status (2 is suspended)
			})
		).json()
		print(disableUser)
		print('user disabled. state: ' + str(disableUser['state']) + ', status: ' + str(disableUser['status']))
	except:
		print('Something broke while disabling ' + email)
print('all done!')
