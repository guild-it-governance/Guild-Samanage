"""
Author: Paul Mealus

v1 09/7/2018
v2 11/7/2018 - Rebuild to include function that gets href for every hardware item


"""


import time
import requests

api_token = input("Paste API token: ")


def hardware_hrefs():
    """
    Gets the hrefs for every computer item in the hardware module
    """
    hardware_url = "https://api.samanage.com/hardwares.json"
    print("Requesting list of all computer inventory... please wait")
    r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    pages = int(r.headers['X-Total-Pages'])
    current_page = 1
    href_list = []
    while current_page <= pages:
        print('Gathering links from page# ' + str(current_page) + " of " + str(pages))
        page_url = hardware_url + "?page=" + str(current_page)
        r = requests.get(page_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in range(0,len(r.json())):
            href_list.append(r.json()[i]['href'])
        current_page += 1
        time.sleep(1)
    return href_list


def hardware_owner_mapper(r):
    """
    Grabs the username and tries to put it into the owner field, r is a request.get return object
    """

    url = r.json()['href']
    owner = r.json()['username'] + "@guildmortgage.net"
    requests.put(url, json={
                            "hardware": {
                                "owner": {
                                            "email": owner,
                                         }
                                        }
                            }
                 , headers={'X-Samanage-Authorization': 'Bearer ' + api_token})



print('\n\nPreparing a request to gather links for all Computer Inventory.\n')
href_list = hardware_hrefs()


for i in href_list:
    try:
        r = requests.get(i, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        print("Updating owner of : {}".format(r.json()['serial_number']))
        hardware_owner_mapper(r)
        time.sleep(0.5)
    except TypeError:
        print("Something is wrong with the username for {}".format(i))

print('\n\nDone updating owners.')
