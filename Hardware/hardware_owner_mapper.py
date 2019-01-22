"""
Author: Paul Mealus

v1 09/7/2018 - Initial build
v2 11/7/2018 - Rebuild to include function that gets href for every hardware item - PJM
v3 11/28/2018 - Combined with location mapper - PJM
v4 1/17/2019 - Refactor and clean up flow by adding main method

"""


import time
import requests
import csv


def hardware_hrefs(api_token):
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
        for i in r.json():
            if not i['department']:
                href_list.append(i['href'])
            elif i['department']['name'] == '6103 - IT Holding':
                pass
            elif i['department']['name'] == '1020 - IT Recycling':
                pass
            else:
                href_list.append(i['href'])
        print(len(href_list))
        current_page += 1
        time.sleep(1)
    return href_list


def hardware_owner_mapper(r, api_token):
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
    time.sleep(0.5)


def loc_mapper(r, api_token):
    """
    If an owner exists, try to update the computer's record to match the owner's site/dept.
    Do nothing if the owner is not mapped. r is a request.get return object
    """
    url = r.json()['href']
    dept = r.json()['owner']['department']['name']
    site = r.json()['owner']['site']['name']
    requests.put(url, json={"hardware":{"site":{"name":site},"department":{"name":dept}}}, headers={'X-Samanage-Authorization': 'Bearer '+ api_token})
    time.sleep(0.5)
    print(url + " Updated")


# def exceptions_to_csv(exceptions_list):
#     with open('exceptions.csv', mode='w') as fout:
#         writer = csv.writer(fout)
#         for i in exceptions_list:
#             writer.writerow(
#                 i['serial_number'], i['username'], i['owner'], i['site'], i['department'])


def main():
    api_token = input("Paste API token: ")
    print('\n\nPreparing a request to gather links for all Computer Inventory.\n')
    href_list = hardware_hrefs(api_token)
    exceptions = []
    for i in href_list:
        try:
            r = requests.get(i, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            print("Updating owner and location of : {}".format(r.json()['serial_number']))
            hardware_owner_mapper(r, api_token)

        except (TypeError, KeyError):
            print("ERROR owner data is incorrect for {}, continuing".format(i))
            exceptions.append((i['serial_number'], i['username'], i['owner'], i['site'], i['department']))

        try:
            loc_mapper(r, api_token)

        except (TypeError, KeyError):
            print("ERROR site/loc data is incorrect for {}, continuing".format(i))
            exceptions.append((i['serial_number'], i['username'], i['owner'], i['site'], i['department']))

    for i in exceptions:
        print(i)
    print("\nAll Done.")


if __name__ == '__main__':
    main()

# TODO Kick out exceptions to a CSV