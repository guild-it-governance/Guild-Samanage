'''
Computer to Owner Location Mapper
Paul Mealus

This script checks the site/dept of its owner. Then sets the
computer's site/dept to the same.

'''
#imports
import requests


#variables
api_token = 'INSERT TOKEN HERE'

#functions

def loc_mapper(href):
    '''
    If an owner exists, try to update the computer's record to match the owner's site/dept. 
    Do nothing if the owner is not mapped.
    '''
    comp_url = href
    try:
        cr = requests.get(comp_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        dept = cr.json()['owner']['department']['name']
        site = cr.json()['owner']['site']['name']
        requests.put(comp_url, json={"hardware":{"site":{"name":site},"department":{"name":dept}}}, headers={'X-Samanage-Authorization': 'Bearer '+ api_token})                                      
        print(comp_url + " Updated")
    except:
        print("No owner - Skipping" + comp_url)
    

def hardware_hrefs():
    '''
    Gets the hrefs for every computer item in the hardware module
    '''
    hardware_url = "https://api.samanage.com/hardwares.json"
    print("Requesting list of all computer inventory... please wait")
    r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})     
    pages = int(r.headers['X-Total-Pages'])
    current_page = 1
    href_list = []
    while current_page <= pages:
        print('Gathering links from page# ' + str(current_page))
        page_url = hardware_url + "?page=" + str(current_page)
        r = requests.get(page_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in range(0,len(r.json())):
            href_list.append(r.json()[i]['href'])
        current_page += 1
    return href_list



#Get a list of hrefs w/ the hardware_hrefs function
hrefs = hardware_hrefs()

#pass each href in href list to the loc_mapper function
for i in hrefs:
    loc_mapper(i)



