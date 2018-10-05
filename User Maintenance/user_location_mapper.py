'''
Paul Mealus

This script reads a csv named "user_loc_map" row for row and
updates a samanage user's information.

Col 1: Samanage ID (SAID), COl 2: dept, Col 3: site
Col 4: cost center (this is one of our custom fields)

'''

import requests
import csv

#api token contained in variable for readability
api_token = 'INSERT TOKEN HERE'

'''
Read user_loc_map.csv row for row. Take the first col (SAID), access the
user's account object and update it with dept, site, and cost center
'''

with open("user_loc_map.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        url = "https://api.samanage.com/users/"+row[0]+".xml"
        if "#N/A" in row:
            continue
        else:
            requests.put(url, json={"user":{"department":{"name":row[2]},"site":{"name":row[3]},
            "custom_fields_values":{"custom_fields_value":[{"name":"Cost Center Number", "value":row[4]}]}}},
            headers={'X-Samanage-Authorization': 'Bearer '+ api_token})
            print(row[0] + " " + row[1] + " Updated")

