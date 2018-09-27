"""
Paul Mealus v1

Important: The current version of this script is scoped to computers/laptops only. Remove other products from the
Lasalle Lease Schedule CSV before trying the import.

Put this script in a directory with only LaSalle lease schedules.
It will take the name of the CSVs (Which should be the least schedule number) and create a lease if they don't
already exist. For any new lease created, it will check to see if the serial number exists in samanage. If
it finds the serial number, it will associate that computer to the lease schedule. If the serial number
does not exist in samange, this script will create a new computer item in cost center 6101 IT Ops
Then it will associate that new computer item to the lease schedule.

"""
#Imports
import requests
import csv
import os

#Global Variables
api_token = "cG1lYWx1c0BndWlsZG1vcnRnYWdlLm5ldA==:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjozMTExMTI1LCJnZW5lcmF0ZWRfYXQiOiIyMDE4LTA1LTAzIDA0OjI5OjE1In0.4iOXvrN0htmYDp-gjET3BoAAOi0mDR_TVLdNQPWRyzmifqJ4hgzad1o8tRFMZYgveQmYZ6SKxVwO2PG90tLtDg"
sn = 'CV8ZM12'

#Functions
def hardware_list():
    '''
    Return a list of every computer object
    '''
    hardware_url = "https://api.samanage.com/hardwares.json"
    print("Requesting list of all computer inventory... please wait")
    r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    pages = int(r.headers['X-Total-Pages'])
    current_page = 37
    obj_list = []
    while current_page <= pages:
        print('Gathering links from page# ' + str(current_page))
        page_url = hardware_url + "?page=" + str(current_page)
        r = requests.get(page_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in range(0,len(r.json())):
            obj_list.append(r.json()[i])
        current_page += 1
    return obj_list

def sn_checker(x, sn):
    for i in range(0, len(x)):
        if sn in x[i].values():
            return True
            break
        else:
            return False

def lease_names():
    dir = os.listdir()
    dir.remove('lease_import.py')
    leases = []
    for i in dir:
        leases.append(i[0:-4])
    return leases

def lease_add(lease_names):
    url = 'https://api.samanage.com/contracts.json'
    r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    contracts = []
    for i in range(0,len(r.json())):
        contracts.append(r.json()[i]['name'])
    print(contracts)





