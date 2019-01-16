"""

disabled user/laptop recovery



"""

# Imports
import requests
import time

# Global
api_token = input("Paste API token: ")
reqemail = input("Enter email of the requester :")

# Functions


def get_inactive_users():
    """Make api get requests to samanage to create list of inactive users"""
    user_list = []
    url = 'https://api.samanage.com/users.json?report_id=8992244&applied=true&enabled%5B%5D=0'
    r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    page = 1
    while r.headers['X-Current-Page'] <= r.headers['X-Total-Pages']:
        url2 = url + '&page=' + str(page)
        r = requests.get(url2, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in r.json():
            print('Gathering data for {}'.format(i['name']))
            user_list.append(i)
        page += 1
    return user_list


def pc_check(user):
    """Given a user object, check if they have a laptop, if they do, return a list of tuples with info for a ticket"""
    url = 'https://api.samanage.com/hardwares.json?report_id=9122646&applied=true&owner%5B%5D=' + str(user['group_ids'][0])
    r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    if not r.json():
        pass
    else:
        print(user['name'])
        ticket_info = []
        for c in r.json():

            if not user['site']:
                ticket = (user['name'], c['serial_number'], "Unknown", "Unknown")
                ticket_info.append(ticket)
            else:
                ticket = (user['name'], c['serial_number'], user['site']['name'], user['site']['description'])
                ticket_info.append(ticket)

        return ticket_info


def open_ticket(user, sn, loc, region):
    """Intake necessary arguments and open a ticket for the hardware recovery group"""
    desc = "Laptop owner {}'s profile appears to be inactive. Please find out owner status and if hardware\
                                           needs to be recovered. SN: {}, Region: {}.".format(user, sn, region)

    requests.post('https://api.samanage.com/incidents.json',
                  json={"incident": {
                            "name": "Recover Laptop SN: {}, Owner: {}, Region: {} ".format(sn, user, region),
                            "requester": {"email": reqemail},
                            "priority": "Low",
                            "assignee_id": 4513425,
                            "site": {"name": loc},
                            "category": {"name":"Hardware"},
                            "subcategory": {"name":"Recovery"},
                            "description": desc
                                    }
                        },
                  headers={'X-Samanage-Authorization': 'Bearer ' + api_token})


# Logic

user_list = get_inactive_users()

for i in user_list:
    user_pcs = pc_check(i)
    if not user_pcs:
        pass
    else:
        for i in user_pcs:
            open_ticket(*i)







