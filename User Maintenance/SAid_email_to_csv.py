'''
Paul Mealus

This script was created because samanage user list exports always append a user's email
with text and we wanted just the email.

Make sure you've exported a csv of samanage ids (SAID) before running this script.
Name the csv "SamanageUserIDs". Put the user ids in the 1st column. User IDs are the
unique identifer for samanage user objects. 

This script uses the samanage api and a csv export of user's SA IDs
to write their id and email to a new csv file

'''
#import python requests and csv library
import requests
import csv

#put api token in a variable for readability
api_token = 'INSERT TOKEN HERE'

#initialize an empty list to hold users
userlist = []

#counter
inc = 0

'''
read SamanageUserIDs.csv for each row make an API request user object using the SAID,
this returns a json payload, accessible as a python dictionary. Put the values for
"id" and "email" into a tuple (to keep order) and append to userlist.
'''

with open("SamanageUserIDs.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        url = "https://api.samanage.com/users/" +row[0]+".json"
        r = requests.get(url, headers={"X-Samanage-Authorization": "Bearer " + api_token})
        userlist.append((r.json()['id'], r.json()['email']))
        inc += 1
        print('User #: '+str(inc)+ " Completed")
        
#iterate over userlist and write each tuple to a row in a new csv
with open("SAID_Email.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(userlist)

print("======Script Complete======")
        



