import requests
import os
import json
import re
import logging
import time
import sys
import pandas as pd
from pygnmi.client import gNMIclient
from fastapi import FastAPI

print("<<<<<<<<<< ARCH NETWORK CONTROLLER >>>>>>>>")
print("<<<<<<<<<< OKAN KARADAG, 2024  >>>>>>>>")
# Variables
HOSTS = [
        ('leaf1', '57400'),
        ('leaf2', '57400'),
        ('spine1', '57400'),
        ('spine2', '57400')
        ]

interface_dict = {}
sys_info_dict = {}
host_info_dict = {}

config_dict = [
        {
            "hostname": "",
            "description": "",
            "version": "",
            "current_datetime": ""
            } 
            ]

CONFIG_DB="configDB.csv"
MONITOR_DB="monitorDB.csv"




def get_lldp():
    pass

def set_telemetry():
    pass

def get_host_info(host):
    with gNMIclient(target=host, username='admin', password='admin',skip_verify=True) as gc:
        result = gc.get(path=['/system/name/host-name'])
        return result

def get_sys_info(host):
    with gNMIclient(target=host, username='admin', password='admin',skip_verify=True) as gc:
        result = gc.get(path=['/system/information'])
        return result

def get_interfaces(host):
    with gNMIclient(target=host,username='admin',password='admin',skip_verify=True) as gc:
        result = gc.get(path=["/interface[name=ethernet-1/1]"])
        return result

# API definitions

app = FastAPI()
@app.get("/get-config")
async def read_root():
    
    data = pd.read_csv(CONFIG_DB)
    return data


if __name__ == '__main__':
    isQuit = False 
    while not isQuit: 
        print("######  NW CONTROLLER INITIALIZED #######\n")
        selection = input("please give your selection: collect hosts(host) or collect  interface(int)s\n")
        if selection == "int":
           # interface_dict = get_interfaces()
            print(interface_dict['notification'][0]['update'][0]['val']['admin-state'])  
            isQuit = True
        else:
            
            for host in HOSTS:
                sys_info_dict = get_sys_info(host)
                host_info_dict = get_host_info(host) 
                #print(sys_info_dict)
               # print(host_info_dict) 
                config_dict[0]["hostname"] = host_info_dict['notification'][0]['update'][0]['val'] 
                config_dict[0]['description'] = sys_info_dict['notification'][0]['update'][0]['val']['description']
                config_dict[0]['version'] = sys_info_dict['notification'][0]['update'][0]['val']['version']
                config_dict[0]['current_datetime'] = sys_info_dict['notification'][0]['update'][0]['val']['current-datetime']
                #print(config_dict) 
                df = pd.DataFrame(config_dict) 
                df.to_csv(CONFIG_DB, mode='a', index=False, header=False)  
           
            print("Config DB is populated !!! \n") 
            print("####### API Server is ready ##########'\n")
            isQuit = False
