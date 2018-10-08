"""
Paul Mealus - v1

This script dumps the list of current departments to csv

"""
import os
import requests
import csv
import time

# variables
api_token = input("Paste API token: ")

# functions
def dept_list():
    '''
    Return a list of every computer object
    '''
    dept_url = "https://api.samanage.com/departments.json"
    print("Requesting list of all departments... please wait")
    r = requests.get(dept_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    pages = int(r.headers['X-Total-Pages'])
    current_page = 1
    obj_list = []
    while current_page <= pages:
        print('Gathering departments from page# ' + str(current_page) + " of " + str(pages))
        page_url = dept_url + "?page=" + str(current_page)
        r = requests.get(page_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in r.json():
            obj_list.append(i['name'])
        current_page += 1
        time.sleep(1)
    return obj_list


def list_write(x):

    with open('depts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in x:
            writer.writerow([i])


obj_list = dept_list()

print('Writing depts.csv to ' + os.getcwd() + '... One moment.')
list_write(obj_list)
print('Done!')