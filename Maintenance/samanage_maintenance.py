"""
by Paul Mealus
v2 10/8/2018 - Logic revision
v3 11/6/2018 - Added the ability to update supervisor
v4 1/8/2018 - Refactor for simplicity/flow and changed input csv file
v5 1/23/2018 - Added functions for checking termed user/laptop recovery tickets

"""

import requests
import csv
import time
import datetime


def main():
    # Overall App flow control
    api_token = input("Paste API token: ")
    date_run = input("Last date run? YYYY-M-DD: ")
    date_run = date_run.split("-")
    date_run = datetime.date(int(date_run[0]), int(date_run[1]), int(date_run[2]))

    start_time = time.asctime()
    user_list = csv_reader()
    site_list = []
    dept_list = []

    for i in user_list:

        dept = dept_checker(i)
        if dept not in dept_list:
            dept_list.append(dept)

        site = site_checker(i)
        if site not in site_list:
            site_list.append(site)

    dept_adder(dept_list, api_token)
    site_adder(site_list, api_token)
    user_updater(user_list, api_token)
    term_list = termed_user_list(date_run, user_list)
    term_ticketer(term_list, api_token)

    stop_time = time.asctime()
    print("Start Time: " + start_time)
    print("Stop Time: " + stop_time)
    print("======Script Complete======")


def termed_user_list(last_date_run, user_list):
    last_date_run = last_date_run
    term_user_list = []
    print('Checking for terms')
    for i in user_list:
        if not i['Term Date']:
            continue
        else:
            term_dt = i['Term Date'].split("/")
            term_dt = datetime.date(int(term_dt[2][:4]), int(term_dt[0]), int(term_dt[1]))
            if term_dt > last_date_run:
                term_user_list.append(i)
            else:
                continue
    return term_user_list


def pc_check(email, api_token):
    """Given a user email, check if they have laptops"""
    comp_list = []
    try:
        url = 'https://api.samanage.com/users.json?email=' + email
        r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        time.sleep(0.5)
        hardware_url = 'https://api.samanage.com/hardwares.json?report_id=9122646&applied=true&owner%5B%5D=' + \
                       str(r.json()[0]['group_ids'][0])
        r = requests.get(hardware_url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        time.sleep(0.5)
        for c in r.json():
            comp_list.append(c['serial_number'])

    except IndexError:
        print("IndexError: Continuing...")

    return comp_list


def term_ticketer(term_list, api_token):

    region_id = {
        "Midwest Region": 3959517,
        "Desktop Support": 3440094,
        "Mountain West Region": 3959515,
        "Northern CA": 3959509,
        "Northwest Region": 3959534,
        "Oregon Region": 3959527,
        "Southeast Region": 3959512,
        "Southern CA": 3440094,
        "Texas Region": 3959521,
        "Texas Region 2": 3959521,
    }

    print('Checking terms for laptops and opening recovery tickets.')

    for i in term_list:

        try:
            comp_list = pc_check(i['Email'], api_token)

            if not comp_list:
                continue
            else:

                print("Opening Ticket for {} {}.".format(i['First Name'], i['Last Name']))
                r = requests.post('https://api.samanage.com/incidents.json',
                              json={"incident": {
                                  "name": "Recover Computer(s): TERM {}, {}".format(i['Last Name'], i['First Name']),
                                  "requester": {"email": 'oktaservice@guildmortgage.net'},
                                  "priority": "Low",
                                  "assignee_id": region_id[i['Region']],
                                  "site": {"name": i['Work Location']},
                                  "category": {"name": "Hardware"},
                                  "subcategory": {"name": "Recovery"},
                                  "description": "Serial Number(s):  " + ', '.join(comp_list) +
                                  "\n\n Please find out what is going on with this computer and coordinate with the\
                                  branch/dept for recovery, re-image, re-deploy, etc.",
                                  "custom_fields_value": {
                                    "custom_fields_values": [
                                      {"name": "Region", "value": i['Region']}
                                        ]}
                              }
                              },
                              headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                print(r.status_code)

        except IndexError:
            print("IndexError: Continuing...")


def csv_reader():
    # Return the Samanage Export CSV in dictionary format
    with open("Samanage Export MWF.csv", 'r') as fin:
        reader = csv.DictReader(fin)
        user_list = []
        for row in reader:
            user_list.append(row)

    return user_list


def dept_checker(i):
    # Check if dept already exists in samanage or inactive list, then add to push list
    if not i['Cost Center#'] or not i['Cost Center']:
        dept = None
    elif 'inactive' in i['Cost Center'].lower():
        dept = None
    else:
        dept = i['Cost Center#'] + ' - ' + i['Cost Center']

    return dept


def site_checker(i):
    if "Agency Temps" in i['Work Location']:
        site = None

    else:
        site_name = i['Work Location']
        location = "{}, {}, {}, {}".format(
            i['Work Loc Address'], i['Work Loc City'], i['Work Loc ST'], i['Work Loc Zip'])
        description = i['Region']
        site = site_name, location, description

    return site


def dept_adder(dept_list, api_token):
    # Check if dept exists in samanage, else push into samanage
    print("\n\n\n\nAdding Departments")

    for i in dept_list:
        try:
            url = 'https://api.samanage.com/departments.json?name=' + i
            r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
            if len(r.json()) == 0:
                url2 = 'https://api.samanage.com/departments.json'
                r2 = requests.post(url2, json={'department': {'name': i, 'description': ''}},
                                   headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                print('Status {} : Department {} loaded to Samanage'.format(r2.status_code, i))
                time.sleep(0.5)
            else:
                print('Status NONE : Department {} already in Samanage'.format(i))
        except TypeError:
            print("WARNING TypeError exception... continuing")


def site_adder(site_list, api_token):
    # Check if site exists in samanage, else push into samanage
    print("\n\n\n\nAdding Sites")
    
    for i in site_list:
        try:
            if i:
                url = 'https://api.samanage.com/sites.json?name=' + str(i[0])
                r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                if len(r.json()) == 0:
                    url2 = 'https://api.samanage.com/sites.json'
                    r2 = requests.post(url2, json={'site': {'name': i[0], 'location': i[1], 'description': i[2],
                                                            'language': '-1', 'business_record': {'id': 45512}}},
                                       headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                    print('Status {} : Site {}, {}, {} loaded to Samanage'.format(r2.status_code, i[0], i[1], i[2]))
                    time.sleep(0.5)

                else:
                    print('Status NONE : Site {} already in Samanage'.format(i))
            else:
                print('Status NONE : Site {} already in Samanage'.format(i))
        except TypeError:
            print("WARNING TypeError exception... continuing")


def user_updater(user_list, api_token):
    print("\n\n\n\nUpdating Users")
    for i in user_list:
        try:
            url = "https://api.samanage.com/users.json?email=" + i['Email']
            r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})

            if len(r.json()) == 1:

                dept = i['Cost Center#'] + ' - ' + i['Cost Center']
                url2 = "https://api.samanage.com/users/" + str(r.json()[0]['id']) + ".json"
                r2 = requests.put(
                        url2, json={"user": {"department": {"name": dept}, "site": {"name": i['Work Location']},
                                             "reports_to": {"email": i['Supervisor Email']},
                                             "custom_fields_values": {
                                                 "custom_fields_value": [
                                                     {"name": "Employee ID", "value": i['EE#']},
                                                     {"name": "Cost Center Number", "value": i['Cost Center#']},
                                                     {"name": "Job Title", "value": i['Job Title']},
                                                     {"name": "Region", "value": i['Region']}]}
                                             }
                                    },
                        headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                print("Status {}: {} has been updated.".format(r2.status_code, i['Email']))
                time.sleep(0.5)

            else:
                print('WARNING {} {} {} is not in Samanage, check user info and Okta'.format(
                    i['Email'], i['First Name'], i['Last Name']))
                time.sleep(0.5)

        except TypeError:
            print('WARNING TypeError received for {} {}'.format(i['email'], i['EE#']))
        except requests.Timeout:
            print('WARNING ConnectionError received for {} {}'.format(i['email'], i['EE#']))
        except TimeoutError:
            print('WARNING TimeoutError received for {} {}'.format(i['email'], i['EE#']))


if __name__ == '__main__':
    main()


# TODO more consistent "NoneType" checks/handling

