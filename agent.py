#! /usr/bin/python3

import requests
import os, sys
import re, uuid
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO) 

def run():
    logging.info("---- Starting | param ----")
    #important variables
    mac_addr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    endpoint = "http://192.168.8.100:5001/heartbeat"
    payload = {'mac_addr':mac_addr}
    ansible_pull_cmd = "sudo ansible-pull -U https://github.com/cliffordolaw/ansible-pull-sample-task.git"

    #Send request to web server    
    try:
        resp = requests.post(endpoint, json=payload, timeout=15) 
        logging.info("Server Response: {}".format(resp.text))
        resp_json = resp.json()
    except Exception as e:
        print(e, file = sys.stderr)
        return
    
    #logging.info("Resp_json[resp]: {}".format(resp_json["resp"]))
    
    #Pull repo for ansible playbook if resp == 0;
    #i.e. it is a new Agent
    if resp_json["resp"] == 0:
        stream = os.popen(ansible_pull_cmd)
        output = stream.read()
        logging.info(output)
        
    
if __name__  == '__main__':
    run()