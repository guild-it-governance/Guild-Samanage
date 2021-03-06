"""
LAMP_Push
by Paul Mealus

Gather all computer inventory from samanage, get the required attributes, then dump into a JSON file for ingest by vendor

"""

import requests
import json


api_token = input("Paste API token: ")


def get_hardware():
    # Return a list of all hardware
    page = 1
    hardware_url = "https://api.samanage.com/hardwares.json?page=" + str(page)
    print("Requesting page " + str(page))
    r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    hw_list = []
    while page <= int(r.headers['X-Total-Pages']):
        for i in r.json():
            hw_list.append(i)
        page += 1
        print("Requesting page " + str(page))
        r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        print(str(page) + " " + r.headers['X-Total-Pages'])
    return hw_list


def info_grab(i):
    # Take a hardware object and grab select attributes, pack dictionary and return it
    try:

        if not i['site']:
            # If there is no site info on the laptop, assign it to corporate
            site = "GRA - Corporate - CA"
            location = "5898 Copley Drive"
        else:
            site = i['site']['name']
            location = i['site']['location']
        if not i['department']:
            # If there is no department info on the laptop, assign it to 6103-IT Holding
            department = "6103 - IT Holding"
        else:
            department = i['department']['name']
            # If there is no owner info on the laptop, assign it to "None"
        if not i['owner']:
            owner = "None"
        else:
            owner = i['owner']['name']

        info = {
            "serial_number": i['bioses'][0]['ssn'],
            "owner": owner,
            "site": site,
            "address": location,
            "cost center - dept": department,
            "latitude": i['latitude'],
            "longitude": i['longitude']
        }

    except TypeError:
        print("Typerror occurred {}".format(i['serial_number']))

    if not info:
        pass
    else:
        return info


hw_list = get_hardware()
lamp_data = []

for i in hw_list:
    lamp_data.append(info_grab(i))

with open("lamp_data_indent.json", "w") as file:
    json.dump(lamp_data, file, indent=4)


# TODO - request.post into endpoint












