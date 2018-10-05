"""
Intake a CSV file, search samanage for each serial # in the lease, if its in samanage tag the
asset's lease schedule custom field w/ lease schedule #

"""

import csv
import requests
import time


api_token = "INSERT TOKEN"

def hardware_list():
    '''
    Return a list of every computer object
    '''
    hardware_url = "https://api.samanage.com/hardwares.json"
    print("Requesting list of all computer inventory... please wait")
    r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    pages = int(r.headers['X-Total-Pages'])
    current_page = 1
    obj_list = []
    while current_page <= pages:
        print('Gathering computer items from page# ' + str(current_page) + " of " + str(pages))
        page_url = hardware_url + "?page=" + str(current_page)
        r = requests.get(page_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in range(0, len(r.json())):
            obj_list.append(r.json()[i])
        current_page += 1
        time.sleep(1)
    return obj_list


def tagger(obj_list, sn):
    in_samanage = False
    for i in range(0, len(obj_list)):
        try:
            if sn in obj_list[i].values():
                requests.put(obj_list[i]['href'],
                             json={"hardware": {"custom_fields_values": {
                                 "custom_fields_value": [{"name": "Lease Schedule #", "value": sch_num}]}}},
                             headers={'X-Samanage-Authorization': 'Bearer '+ api_token})
                in_samanage = True
                time.sleep(.5)
                break
            else:
                pass
        except (TypeError, ValueError, TimeoutError):
            print("TypeError, ValueError, TimeoutError Detected: " + sn)
    if in_samanage:
        print(sn + " updated")
    else:
        print(sn + " not in Samanage")


sch_num = input("\n\nWhich lease schedule would you like to tag?: ")

obj_list = hardware_list()

print("=" * 35)
print("Done collecting hardware, now processing lease schedule " + sch_num)
print("=" * 35)

with open("SCHE " + sch_num + '.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        tagger(obj_list, row[1])
