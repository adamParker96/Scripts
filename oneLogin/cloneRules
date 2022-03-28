import requests
import json
from datetime import datetime
import csv

todayDate = datetime.today().strftime('%m-%d-%Y')
oneLoginAuth = "client_id : CLIENT_ID, " \
               "client_secret : CLIENT_SECRET"
appID = APP_ID  ##change this to specify what app you wanna pull rules from
newAppID = NEW_APP_ID  ##change this to specify what app you wanna push rules to
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

## map old role values to new role values in a dictionary
roleDict = {}
oldRoles = requests.get(
            url='https://api.us.onelogin.com/api/2/apps/' + str(appID) + '/rules/actions/set_role/values',
            params={
            },
            headers={
                "Authorization": "bearer " + oAuth,
                "Content-Type": "application/json"
            },
        ).json()
print('oldRoles: ' + str(oldRoles))

newRoles = requests.get(
            url='https://api.us.onelogin.com/api/2/apps/' + str(newAppID) + '/rules/actions/set_role/values',
            params={
            },
            headers={
                "Authorization": "bearer " + oAuth,
                "Content-Type": "application/json"
            },
        ).json()
print(newRoles)

for role in oldRoles:
  for role2 in newRoles:
    if role2['name'] == role['name']:
      roleDict[role['value']] = role2['value']
print(roleDict)
print('----------------------------------------------------------------------------------')

## now that we've set up our dict, we need to pull the rules we want to clone
getRules = requests.get(
            url='https://api.us.onelogin.com/api/2/apps/' + str(appID) + '/rules',
            params={
            },
            headers={
                "Authorization": "bearer " + oAuth,
                "Content-Type": "application/json"
            },
        ).json()

## once all the rules have been pulled, we iterate through and add them into our app
url2 = "https://api.us.onelogin.com/api/2/apps/newAppID/rules"
for rule in getRules:
    i = 0
    ## go through our dictionary(s) and swap in the new values
    for action in rule['actions']:
        if 'role' in str(action['action']):
            value = action['value']
            rule['actions'][i]['value'] = [roleDict[value[0]]]
            i += 1
            continue
    params = json.dumps({
            "name": rule['name'],
            "match": rule['match'],
            "enabled": rule['enabled'],
            "position": None,
            "conditions": rule['conditions'],
            "actions":  rule['actions']
        })
    print(params)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + oAuth,
        'Cookie': 'ol_mappings_api_service_canary_7=false'
    }
    response = requests.request("POST", url2, headers=headers, data=params)

print(response.json())
print('done')
