#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Aman Varma     amanvarma993@gmail.com
"""
#----------------------- Parameters to change ----------------------

min_age_limit = 45

# There is a rate limit of 100 queries per 5 min on the website.
attempts_per_minute = 2   # Number of attempts in one minute for all days                         
#-------------------------------------------------------------------
import os
import requests
import datetime
import time 
from sys import platform
import mysql.connector
import email_notification 

def encode_key(email, pin_code):
    key = str(email) + " " + str(pin_code)
    return key

def update_available_pin_code_email_mapping(message, email_list, pin_code):
    for email in email_list:
        key = encode_key(email,pin_code)
        pin_code_email_mapping[key][0] = message
        pin_code_email_mapping[key][2] = True

def reset_pin_code_email_mapping():
    for key in pin_code_email_mapping:
        pin_code_email_mapping[key][3] = False
 
def update_pin_code_email_mapping(results, pin_codes_to_check):
    for x in results:
        email = x[1]
        pin_code = x[2]
        key = encode_key(email, pin_code) 
        if key in pin_code_email_mapping:
            pin_code_email_mapping[key][0] = ""
            pin_code_email_mapping[key][2] = False
            pin_code_email_mapping[key][3] = True 
        else:
            pin_code_email_mapping[key] = ["",0,False,True]

        if pin_code in pin_codes_to_check:
           pin_codes_to_check[pin_code].append(email)
        else:
           pin_codes_to_check[pin_code] = [email] 

def read_from_database():
    mydb = mysql.connector.connect(
      host="localhost",
      user="springstudent",
      password="springstudent",
      database="user_directory"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user")
    results = mycursor.fetchall()
    return results

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

pin_code_email_mapping = {}      # { pin_code : { email : [message, in_database, ] } }
attempt = 1
while True:
    today = datetime.date.today().strftime('%d-%m-%Y')
    print ("Checking for available slots: Attempt " + str(attempt))
    available_pin_codes = {}
    pin_codes_to_check = {}

    reset_pin_code_email_mapping()
    results = read_from_database()
    update_pin_code_email_mapping(results, pin_codes_to_check)

    for pin_code in pin_codes_to_check:
        PARAMS = {'pincode':pin_code, 'date':today}
        try:
            r = requests.get(url = url,params=PARAMS, headers=headers)
            responses = r.json()
            for centers in responses['centers']:
                for data in centers['sessions']:
                    if (int(data['min_age_limit']) == min_age_limit and int(data['available_capacity']) > 0):
                        message = "----------- date: " + data['date'] + " ----------- pin code: " + str(pin_code) + " -----------\n" 
                        message += "Center: " + centers['name'] + "\n"
                        message += "Min Age Limit: " + str(data['min_age_limit']) + "\n"
                        message += "Available Capacity: " + str(data['available_capacity']) + "\n"
                        message += "Slots: " + str(data['slots']) + "\n\n"
                        update_available_pin_code_email_mapping (message, pin_codes_to_check[pin_code] ,pin_code)    
        except Exception as e:
            print("ERROR:" + str(e))
            continue
   
    attempt += 1
    email_notification.notify(pin_code_email_mapping)
            
    time.sleep(int(60/attempts_per_minute))

