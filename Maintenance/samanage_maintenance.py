'''
Paul Mealus
v2 10/8/2018
v3 11/6/2018 - Added the ability to update supervisor

'''

import requests
import csv
import time

start_time = time.asctime()

api_token = input("Paste API token: ")


site_list = []
dept_list = []
inact_dept_list = []

print('Generating site and department lists... please wait')

with open("Business Continuity - Employee Information.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            if row[0] == "Name":
                continue

            dept = row[10] + ' - ' + row[9]
            if 'inactive' in dept.lower():
                if dept not in inact_dept_list:
                    inact_dept_list.append(dept)
                else:
                    continue
            elif dept not in dept_list:
                dept_list.append(dept)
            else:
                continue

            site = (row[18], row[19], row[8])
            if site not in site_list:
                site_list.append(site)
            else:
                continue

        except:
            print("Timeout error... continuing")
            time.sleep(0.5)

print("Adding new sites to Samanage... please wait")
try:

    for i in site_list:
        url = 'https://api.samanage.com/sites.json?name=' + str(i[0])
        r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        if len(r.json()) == 0:
            url2 = 'https://api.samanage.com/sites.json'
            r2 = requests.post(url2, json={'site': {'name': i[0], 'location': i[1], 'description': i[2],
                                                    'language': '-1', 'business_record': {'id': 45512}}},
                               headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            print('Status {} : Site {}, {}, {} loaded to Samanage'.format(r2.status_code, i[0], i[1], i[2]))
        else:
            print('Site {}, {}, {} already in Samanage'.format(i[0], i[1], i[2]))
            continue

    print("\n" * 5)
    print("Adding new departments to Samanage... please wait\n")

except:
    print("Timeout error... continuing")
    time.sleep(0.5)

try:

    for i in dept_list:
        url = 'https://api.samanage.com/departments.json?name=' + i
        r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        if len(r.json()) == 0:
            url2 = 'https://api.samanage.com/departments.json'
            r2 = requests.post(url2, json={'department': {'name': i, 'descripition': ''}},
                               headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            print('Status {} : Department {} loaded to Samanage'.format(r2.status_code, i))
        else:
            print('Department {} already in Samanage'.format(i))
            continue

    print("\n" * 5)
    print("Done with site and departments\n")

except:
    print("Timeout error... continuing")
    time.sleep(0.5)


print("Working on Employee Data...")

with open("Business Continuity - Employee Information.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:

        if row[0] == "Name":
            continue

        dept = row[10] + ' - ' + row[9]
        site = row[18]
        mgr = row[12]

        try:
            url = "https://api.samanage.com/users.json?email=" + row[17]
            r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            if len(r.json()) == 1:
                url2 = "https://api.samanage.com/users/" + str(r.json()[0]['id']) + ".json"
                r2 = requests.put(
                    url2, json={"user": {"department": {"name": dept}, "site": {"name": site},
                                         #"reports_to":{"email":mgr},
                                         "custom_fields_values": {
                                             "custom_fields_value": [
                                                 {"name": "Employee ID", "value": row[1]},
                                                 {"name": "Cost Center Number", "value": row[10]}]}
                                         }
                                },
                    headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                print("HTTP {} : {} checked/updated".format(r2.status_code, row[17]))
            else:
                print("HTTP {} : {} Not in Samanage, check Okta".format(r.status_code, row[17]))
                continue
        except:
            print("Unable to update : {}, check if they exist in Samanage and Okta".format(row[17]))

stop_time = time.asctime()

print("Start Time: " + start_time)
print("Stop Time: " + stop_time)
print("======Script Complete======")
