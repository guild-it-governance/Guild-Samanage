'''
Paul Mealus
v2 - 10/8/2018

This script was created because samanage user list exports always append a user's email
with a blob of text and we wanted just the email.

Make sure you've exported a csv of samanage users before running this script. You will need
to edit the CSV so the samanage user ids are in the first column.

Name the csv "samanage_user_ids". Make sure the user IDs are in the 1st column, the
rest of the columns can be blank. User IDs are the unique identifier for samanage user
objects. Make sure the csv is in the same folder as this script.

This script uses the samanage api and a csv export of user's SA IDs
to write their id and email to a new csv file

'''

#import python requests and csv library
import requests
import csv
import os

#put api token in a variable for readability
api_token = input("Paste API token: ")

#initialize an empty list to hold users
userlist = []

#counter
inc = 0

'''
read samanage_user_ids.csv for each row make an API request user object using the SAID,
this returns a json payload, accessible as a python dictionary. Put the values for
"id" and "email" into a tuple (to keep order) and append to userlist.
'''

with open("samanage_user_ids.csv", "r", newline="") as f:
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

print("SAID_Email.csv has been created in " + os.getcwd())
print("======Script Complete======")
        



