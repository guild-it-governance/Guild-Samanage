'''
Paul Mealus
For non scheduled updates via csv

v2 10/8/2018
v3 11/6/2018 - Added the ability to update supervisor
v4 11/30/2018 - Added the ability to update region and job title

'''

import requests
import csv
import time

start_time = time.asctime()

api_token = input("Paste API token: ")


with open("User Data.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:

        emplid = row[0]
        name = row[1]
        # samid = row[2]
        site = row[3]
        dept = row[4]
        # ccn = row[5]
        mgr = row[5]
        # reg = row[7]
        # job = row[8]
        email = row[2]

        try:
            geturl = "https://api.samanage.com/users.json?email=" + email
            getr = requests.get(geturl, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            url = "https://api.samanage.com/users/" + str(getr.json()[0]['id']) + ".json"
            r = requests.put(
                url, json={"user": {"department": {"name": dept}, "site": {"name": site},
                                    "reports_to": {"email": mgr},
                                    "custom_fields_values": {
                                        "custom_fields_value": [
                                            {"name": "Employee ID", "value": emplid},
                                            {"name": "Cost Center Number", "value": 0},
                                            ]}
                                    }
                           },
                headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            print("Status {}: {} Updated ".format(r.status_code, name))

        except:
            print("Unable to update : {}, {} check if they exist in Samanage and Okta".format(name, email))

stop_time = time.asctime()

print("Start Time: " + start_time)
print("Stop Time: " + stop_time)
print("======Script Complete======")
