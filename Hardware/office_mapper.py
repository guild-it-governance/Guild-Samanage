import requests
import csv


def main():
    api_token = input("Paste API token: ")
    ids_list = csv_reader()
    pc_list = []
    for id in ids_list:
        url = 'https://api.samanage.com/hardwares/' + id['id'] + '.json'
        r = get(url, api_token)
        pc_info = info_get(r, api_token)
        pc_list.append(pc_info)
    csv_writer(pc_list)


def csv_reader():
    # Return the Samanage Export CSV in dictionary format
    with open("ids.csv", 'r') as fin:
        reader = csv.DictReader(fin)
        ids_list = []
        for row in reader:
            ids_list.append(row)

    return ids_list


def csv_writer(pc_list):
    with open('win10_hw.csv', 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerows(pc_list)


def get(url, api_token):
    r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
    return r


def info_get(r, api_token):
    print("Getting hardware info " + r.json()['name'])
    pc_info = []

    pc_info.append(r.json()['name']                     )
    pc_info.append(r.json()['serial_number']            )
    pc_info.append(r.json()['model']                    )
    pc_info.append(r.json()['bioses'][0]['ssn']         )
    pc_info.append(r.json()['bioses'][0]['manufacturer'])
    pc_info.append(r.json()['bioses'][0]['model']       )
    memories = []
    for i in r.json()['memories']:
        memories.append(i['capacity'])
    pc_info.append(memories)
    pc_info.append(r.json()['operating_system']           )
    pc_info.append(r.json()['operating_system_version']   )
    softwares = software_get(r.json()['softwares_href'], api_token)
    pc_info.append(softwares)

    try:
        pc_info.append(r.json()['username']                   )
        pc_info.append(r.json()['owner']['name']              )
        pc_info.append(r.json()['owner']['email']             )
        pc_info.append(r.json()['owner']['site']['name']      )
        pc_info.append(r.json()['owner']['department']['name'])

    except Exception as err:
        print("Passing...")
    return pc_info


def software_get(software_href, api_token):
    print("Getting software...")
    url1 = software_href + '?page=1'
    url2 = software_href + '?page=2'
    url3 = software_href + '?page=3'
    url4 = software_href + '?page=4'

    urls = [url1, url2, url3, url4]
    software_list = []
    for url in urls:
        r = requests.get(url, headers={'X-Samanage-Authorization': 'Bearer ' + api_token})
        for i in r.json():
            if "Microsoft Office" in i['name']:
                software_list.append(i['name'] + " " + i['version'])

    return software_list


if __name__ == '__main__':
    main()