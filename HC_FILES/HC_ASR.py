"""
<PYATS_JOBFILE>
"""
import sys
import os
from pyats.easypy import run
import time
from datetime import datetime, timedelta
from pyats.easypy import Task
from genie.testbed import load
import argparse
import yaml

parser = argparse.ArgumentParser(description = "HC_param")
parser.add_argument('--customer_param', help = 'Add Param for failed')
parser.add_argument('--nodes', help = 'Add Param for failed')
parser.add_argument('--hc_type', help = 'Add Param for failed')

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

# All run() must be inside a main function
def main(runtime,):
    task_number={1,2,3,4}
    args = parser.parse_args()
    with open(args.customer_param) as f:
        dataMap = yaml.safe_load(f)
    HC_obj=Struct(**dataMap)
    testbed = load (args.nodes)
    #testbed = load ("leo.yml")
    runtime.job.name = HC_obj.customer_name
    #device_actual = testbed.devices['MXAPOM01SPGW01']
    #run(testscript='/healthcheck/testcase/gHC.py', runtime = runtime, device=device_local)
    # Execute the testscript
    dev_list=[]
    for device in testbed:
        dev_list.append(device)
    exec_n=0
    exec_tot= len(dev_list)
    task_number=[1,2,3,4]
    task_id={}
    while exec_n != exec_tot:
        counter = timedelta(minutes = 5)
        for id in task_number:
            if exec_n != exec_tot:
                task_id[id]= Task(testscript='/healthcheck/testcase/{}'.format(args.hc_type), runtime = runtime, device=dev_list[exec_n],taskid=dev_list[exec_n].name, HC_param=HC_obj)
                exec_n+=1
                task_id[id].start()
        while counter:
            if task_id[1].is_alive() or task_id[2].is_alive() or task_id[3].is_alive() or task_id[4].is_alive(): 
            #if task_1.is_alive() or task_2.is_alive() or task_3.is_alive() or task_4.is_alive():
                time.sleep(1)
                counter -= timedelta(seconds=1)
            else:
                break

