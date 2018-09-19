'''
Paul Mealus

This script intakes hw_map.csv with the asset's id (exported from samanage) and
active directory or workgroup username.
The csv should be structured like this:

Col 1: Samanage asset ID (7 digits), Col2: Username, Col3: Email Address

Then it inputs the email address (since email is a unique owner identifier
into the "owner" field.


Future State:
Skip the csv and request a list of all assets. For each asset check if owner
exists, if not map the user to an email address and input the address
in owner field. Add a try except block for error handling. Tie this into the
computer_location_mapper script
'''
import csv
import requests

api_token = 'INSERT TOKEN HERE'

with open ('hw_map.csv', newline='') as f:
    rdr = csv.reader(f)
    for row in rdr:
        url = 'https://api.samanage.com/hardwares/'+row[0]+'.json'
        r = requests.put(url, json={"hardware":{"owner":{"email":row[2]}}}, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        print(row[0] + " " + str(r.status_code) + " " + r.reason)
