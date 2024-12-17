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
from pydantic import BaseModel

print("<<<<<<<<<< ARCH NETWORK CONTROLLER >>>>>>>>")
print("<<<<<<<<<< OKAN KARADAG, 2024  >>>>>>>>")
# Variables
# routers should be available,here containerlab is used
HOSTS = [
        ('leaf1', '57400'),
        ('leaf2', '57400'),
        ('spine1', '57400'),
        ('spine2', '57400')
        ]

node_cert =  "./cert/leaf1.pem"
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
#configuration database
CONFIG_DB="configDB.csv"

#telemetry database
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


def set_host_name(host: str,name: str):
    
    u = [
    (
        "openconfig:/system/name",
        {"host-name":  name},
    )
   ] 
   # path_cert = node_cert if tls is used 
   # skip_verify = True for bypassing tls 
    with gNMIclient(target=host,username='admin',password='admin',path_cert = node_cert) as gc:
        result = gc.set(update=u)
        print(result)


# API definitions

app = FastAPI()
# api input model definition alinged with pydantic
class Config(BaseModel):
    node: str
    param: str 
    value: str


@app.get("/get-config")
async def get_config():
    data = pd.read_csv(CONFIG_DB)
    return data


@app.post("/set-config/")
async def set_config(cfg: Config):
    return cfg


@app.put("/update-config/")
async def update_config(cfg: Config):
    data = pd.read_csv(CONFIG_DB)
    for (index,row) in data.iterrows():
        if row.hostname == cfg.node:
            data.at[index,cfg.param] = cfg.value 
    data.to_csv(CONFIG_DB, index=False)
    if cfg.param == "hostname":
        host=(cfg.node,"57400") 
        set_host_name(host,cfg.value)


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
                config_dict[0]["hostname"] = host_info_dict['notification'][0]['update'][0]['val'] 
                config_dict[0]['description'] = sys_info_dict['notification'][0]['update'][0]['val']['description']
                config_dict[0]['version'] = sys_info_dict['notification'][0]['update'][0]['val']['version']
                config_dict[0]['current_datetime'] = sys_info_dict['notification'][0]['update'][0]['val']['current-datetime']
                df = pd.DataFrame(config_dict) 
                df.to_csv(CONFIG_DB, mode='a', index=False, header=False)  
           
            print("Config DB is populated !!! \n") 
            print("####### API Server is ready ##########'\n")
            isQuit = False
