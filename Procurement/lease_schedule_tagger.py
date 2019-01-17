"""
Intake a CSV file, search samanage for each serial # in the lease, if its in samanage tag the
asset's lease schedule custom field w/ lease schedule #

"""

import csv
import requests
import time


def tagger(href_list, sch_num, api_token):
    for i in href_list:
        r = requests.put(i,
                     json={"hardware": {"custom_fields_values": {
                         "custom_fields_value": [{"name": "Lease Schedule #", "value": sch_num}]}}},
                     headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        time.sleep(0.5)
        print(r.status_code, i, "Updated")


def serial_checker(dev_list, api_token):
    # Check if serial exists in samanage
    in_list = []
    for i in dev_list:
        if not i['Serial Number']:
            pass
        else:
            try:
                sn = i['Serial Number']
                url = "https://api.samanage.com/hardwares.json?report_id=9122646&applied=true&serial_number%5B%5D=" + sn
                print("Requesting {}".format(i))
                r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
                time.sleep(0.5)
                if len(r.json()) == 1:
                    in_list.append(r.json()[0]['href'])
                    print("{} added to update list".format(sn))

            except TimeoutError:
                print("TimeoutError: Passing")
            except ConnectionAbortedError:
                print("ConnectionAbortedError: Passing")
            except ConnectionError:
                print("ConnectionError: Passing")
            except Exception as err:
                print(err)

    return in_list


def csv_reader(name):
    # Return the Samanage Export CSV in dictionary format
    with open(name + ".csv", 'r') as fin:
        reader = csv.DictReader(fin)
        dev_list = []
        for row in reader:
            dev_list.append(row)

    return dev_list


def main():
    api_token = input("Paste API token: ")
    sch_num = input("Which lease schedule would you like to tag?: ")
    dev_list = csv_reader(sch_num)
    href_list = serial_checker(dev_list, api_token)
    tagger(href_list, sch_num, api_token)


if __name__ == '__main__':
    main()
