from api_func import *
from configs import *
from pathlib import Path
from datetime import datetime
import os
import json
import jwt
import requests
import urllib3
import multiprocessing
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent


def global_query(data,query):
    # test_result = TestResult()
    # log.info(str(PROJECT_ROOT))
    
    stack_keys = open_js_safely(api_path)
    mglobal_query_api = query_api.format(data['domain'],data['domainSuffix'],data['customerId'])
    pl=query.format(load_start,load_end)
    payload["query"]=pl
    
    output2 = post_api(data,mglobal_query_api,payload)
    job_id= output2['id']
    n_result_api =result_api.format(data['domain'], data['domainSuffix'], data['customerId'],job_id)
    payload["query"]=""

    if output2['status']=="FINISHED":
        return response
    else:
        while output2['status'] not in ['FINISHED', 'ERROR']:
            time.sleep(10)
            n_api=mglobal_query_api+'/'+job_id
            output2=get_api(data,n_api)
        if output2['status'] == 'ERROR':
            print('global query failed' )
        else :
            response=get_api(data,n_result_api)
            return response
            
def execute_query(customer, query,event_count):
    
    resp = global_query(customer,query)
    
    
    with event_count.get_lock():
        event_count.value += resp["items"][0]["rowData"]["_col0"]
    
def format_count(count):
    if count >= 10**6:
        return f"{count / 10**6:.2f} million"
    elif count >= 10**3:
        return f"{count // 10**3}k"
    else:
        return count

def assume_role(data):
    query = "select count(*) from aws_cloudtrail_events where upt_time >= timestamp '{}' and upt_time <= timestamp '{}' and upt_day > 20230728 and event_name='AssumeRole';"
    processes = []
    event_count = multiprocessing.Value('i', 0)
    for customer in json.loads(data):
            p = multiprocessing.Process(target=execute_query, args=(customer, query,event_count))
            p.start()
            processes.append(p)
    for p in processes:
        p.join(timeout=20)
    
    
    print(f"Total assume role records: {format_count(event_count.value)}")
    print(f"Total assume role records/hour: {format_count(event_count.value / 12)}")





def akia(data):
    query = "select count(*) from aws_cloudtrail_events where upt_time >= timestamp '{}' and upt_time <= timestamp '{}' and upt_day > 20230728 and event_name='AssumeRole' and user_identity_access_key_id like 'AKIA%';"
    processes = []
    event_count = multiprocessing.Value('i', 0)
    unique = multiprocessing.Value('i', 0)
    for customer in json.loads(data):
            p = multiprocessing.Process(target=execute_query, args=(customer, query,event_count))
            p.start()
            processes.append(p)
    for p in processes:
        p.join(timeout=20)
    
    
    

    query = "SELECT COUNT(DISTINCT user_identity_access_key_id) FROM aws_cloudtrail_events WHERE upt_time >= TIMESTAMP '{}' AND upt_time <= TIMESTAMP '{}'AND upt_day > 20230728 AND event_name = 'AssumeRole' AND user_identity_access_key_id LIKE 'AKIA%';"

    for customer in json.loads(data):
            p = multiprocessing.Process(target=execute_query, args=(customer, query,unique))
            p.start()
            processes.append(p)
    for p in processes:
        p.join(timeout=20)
    
    
    print(f"\nAssumeRole generated by AKIA: {format_count(event_count.value)} with unique AKIA keys: {format_count(unique.value)}")
    print(f"AssumeRole generated by AKIA/hour: {format_count(event_count.value / 12)}")

def asia(data):
    query = "select count(*) from aws_cloudtrail_events where upt_time >= timestamp '{}' and upt_time <= timestamp '{}' and upt_day > 20230728 and event_name='AssumeRole' and user_identity_access_key_id like 'ASIA%';"
    processes = []
    event_count = multiprocessing.Value('i', 0)
    
    for customer in json.loads(data):
            p = multiprocessing.Process(target=execute_query, args=(customer, query,event_count))
            p.start()
            processes.append(p)
    for p in processes:
        p.join(timeout=20)
    
    print(f"\nAssumeRole generated by ASIA: {format_count(event_count.value)}")
    print(f"AssumeRole generated by ASIA/hour: {format_count(event_count.value/12)}")

def services(data):
    query = "select count(*) from aws_cloudtrail_events where upt_time >= timestamp '{}' and upt_time <= timestamp '{}' and upt_day > 20230728 and event_name='AssumeRole' and user_identity_access_key_id is NULL;"
    processes = []
    event_count = multiprocessing.Value('i', 0)
    for customer in json.loads(data):
            p = multiprocessing.Process(target=execute_query, args=(customer, query,event_count))
            p.start()
            processes.append(p)
    for p in processes:
        p.join(timeout=20)
    
    
    print(f"\nAssumeRole generated by services: {format_count(event_count.value)}")
    print(f"AssumeRole generated by services/hour: {format_count(event_count.value / 12)}")



if __name__=="__main__":
    fs = open(api_path)
    file = fs.read()

    
    assume_role(file)
    akia(file)
    asia(file)
    services(file)