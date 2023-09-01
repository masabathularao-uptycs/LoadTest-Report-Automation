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


def global_query(data,table):
    # test_result = TestResult()
    # log.info(str(PROJECT_ROOT))
    print(table)
    stack_keys = open_js_safely(api_path)
    mglobal_query_api = query_api.format(data['domain'],data['domainSuffix'],data['customerId'])
    pl=payload["query"].format(table,load_start,load_end)
    payload["query"]=pl
    output2 = post_api(data,mglobal_query_api,payload)
    job_id= output2['id']
    n_result_api =result_api.format(data['domain'], data['domainSuffix'], data['customerId'],job_id)
    payload["query"]="select upt_added,count(*) from {} where upt_day >= 2022-07-13 and upt_time >= timestamp '{}' and upt_time < timestamp '{}' group by upt_added;"

    if output2['status']=="FINISHED":
        response=get_api(data,n_result_api)
        print(response['items'][0]['rowData']['_col0'])
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
            

def expected():
    
    for filename in os.listdir(json_directory):
        if filename.endswith(".json"):
            with open(os.path.join(json_directory, filename), "r") as file1:
                data = json.load(file1)
            
            
            for table_name, table_values in data.items():
                if table_name in total_counts:
                    for operation, count in table_values.items():
                        total_counts[table_name][operation] += count





def execute_query(table,customer, event_count, upt_added_true, upt_added_false):
    
    resp = global_query(customer,table)
    
    if "aws_cloudtrail_events" in query_api:
        with event_count.get_lock():
            event_count.value += resp["items"][0]["rowData"]["_col0"]
    else:
        for item in resp["items"]:
            upt_added = item["rowData"]["upt_added"]
            count = item["rowData"]["_col1"]
            if upt_added:
                with upt_added_true.get_lock():
                    upt_added_true.value += count
            else:
                with upt_added_false.get_lock():
                    upt_added_false.value += count



def table_accuracy(data, table, actual_true_count,actual_false_count,expected_true_count,expected_false_count):
    accuracy_true = round((actual_true_count / expected_true_count) * 100, 2)
    accuracy_false= round((actual_false_count / expected_false_count) * 100, 2)
    accuracy_entry = {"table": table, "UPT_added_true":actual_true_count, "UPT_added_false": actual_false_count, "Expected_added_true":expected_true_count, "Expected_added_false": expected_false_count,  "accuracy true": accuracy_true, "aaccuracy false":accuracy_false}
    #accuracy_entry={"table": table,  "expected added": expected_true_count, "expected deleted": expected_false_count}
    data.append(accuracy_entry)

def tables_accuracy(data,file):
    
    customer=json.loads(file)
    for table in total_counts:
        response = global_query(customer,table)  
        if table=='aws_cloudtrail_events':
            
            actual_true_count= response['items'][0]['rowData']['_col1']
            actual_false_count=1
        else:
            if response['items'][0]['rowData']['upt_added'] == True:
                
                actual_true_count= response['items'][0]['rowData']['_col1']
                actual_false_count= response['items'][1]['rowData']['_col1']
            else:
                actual_true_count= response['items'][1]['rowData']['_col1']
                actual_false_count= response['items'][0]['rowData']['_col1']


        expected_true_count = total_counts[table].get("added", 1)  
        expected_false_count = total_counts[table].get("removed", 1) 
        table_accuracy(data, table, actual_true_count,actual_false_count,expected_true_count,expected_false_count)

def multi_accuracy(data,file):
    
    for table in total_counts:
        
        upt_added_true = multiprocessing.Value('i', 0)
        upt_added_false = multiprocessing.Value('i', 0)
        event_count = multiprocessing.Value('i', 0)
        processes = []

        for customer in json.loads(file):
            p = multiprocessing.Process(target=execute_query, args=(table,customer, event_count, upt_added_true, upt_added_false))
            p.start()
            processes.append(p)
            
        
        for p in processes:
            p.join(timeout=20)

    
    
            
        
        

        expected_true_count = total_counts[table].get("added", 1)  
        expected_false_count = total_counts[table].get("removed", 1)
        table_accuracy(data, table, upt_added_true.value,upt_added_false.value, expected_true_count,expected_false_count)
       




def single_tables_accuracy_xl(file):
    expected_data = []
    expected()
    tables_accuracy(expected_data,file)
    df = pd.DataFrame(data=expected_data)
    df.to_excel("excelsheets/" + domain + "single_tables_accuracy.xlsx", index=False)

def multi_tables_accuracy_xl(file):
    expected_data = []
    expected()
    multi_accuracy(expected_data,file)
    df = pd.DataFrame(data=expected_data)
    df.to_excel("excelsheets/" + domain + "multi_tables_accuracy.xlsx", index=False)

   
if __name__=="__main__":
    fs = open(api_path)
    file = fs.read()

    #single_tables_accuracy_xl(file)
    multi_tables_accuracy_xl(file)