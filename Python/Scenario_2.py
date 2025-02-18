#Importing necessary libraries

import psycopg2
import requests
import apachelogs
import apache_log_parser
from datetime import datetime
from user_agents import parse

log_parser = apache_log_parser.make_parser('%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"')

file_path = "access_logs_file.txt"                            

def database_connect(data_list):

    try:
        conn = psycopg2.connect(
        host="localhost",
        database="scenario2_db",
        user="postgres",   
        password="newpassword"
        )
        cursor = conn.cursor()
        print("Connection Established")
        
        query= """INSERT INTO access_logs(ip_address, date_time, http_method, url_path, status_code, referer, user_agent, browser, os)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        insert_data=[]
        
        for data in data_list:
            insert_data.append((
                data["ip_address"],
                data["date_time"],
                data["http_method"],
                data["url_path"],
                data["status_code"],
                data["referer"],
                data["user_agent"],
                data["browser"],
                data["os"]))

        cursor.executemany(query,insert_data)
        conn.commit()
        print("Logs Data has been successfully inserted")

    except Exception as e:
        print("Error:",e)

    finally:
        
        cursor.close()
        conn.close()

with open("apache_logs_file.txt","r") as file:

    lines=file.readlines()
    
    complete_logs_data=[]
    
    for logs in lines:
        
         fetched_logs = log_parser(logs)
         brackets_time = fetched_logs['time_received'][1:-1]
         user_agent_data=fetched_logs.get('request_header_user_agent')

         extract_logdata={
             
            "ip_address": fetched_logs["remote_host"],
            "date_time": datetime.strptime(brackets_time, "%d/%b/%Y:%H:%M:%S %z"),
            "http_method": fetched_logs["request_method"],
            "url_path": fetched_logs["request_url"],
            "status_code": fetched_logs["status"],
            "referer": fetched_logs.get("request_header_referer"),
            "user_agent": user_agent_data,
            "browser":parse(user_agent_data).browser.family,
            "os": parse(user_agent_data).os.family
            }
         complete_logs_data.append(extract_logdata)
            
    if complete_logs_data:
        database_connect(complete_logs_data)

    else:
        print("Failed to read the data from the file")

