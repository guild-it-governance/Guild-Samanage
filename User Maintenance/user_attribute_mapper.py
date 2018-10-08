'''
Paul Mealus
v2 10/8/2018

This script reads a csv named "user_attrib_map" row for row and
updates a samanage user's information.

Col 1: Samanage ID (SAID), COl 2: email, Col 3: Employee ID,
Col 4: cost center # + cost center descrip, Col 5: Site (Aka work location)

'''

import requests
import csv

#api token contained in variable for readability
api_token = input("Paste API token: ")

'''
Read user_attrib_map.csv row for row. Take the first col (SAID), access the
user's account object and update it with dept, site, and cost center
'''
try:
    with open("user_attrib_map.csv", "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            url = "https://api.samanage.com/users/"+row[0]+".xml"
            if "#N/A" in row:
                continue
            else:
                requests.put(url, json={"user":{"department":{"name":row[3]},"site":{"name":row[4]},
                "custom_fields_values":{"custom_fields_value":[{"name":"Employee ID", "value":row[2]}]}}},
                headers={'X-Samanage-Authorization': 'Bearer '+ api_token})
                print(row[0] + " " + row[1] + " Updated")
except:
    print("Something went wrong with " + row[0] )

print("======Script Complete======")

