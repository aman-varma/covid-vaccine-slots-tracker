#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Aman Varma     amanvarma993@gmail.com
"""
#----------------------- Parameters to change ----------------------

pin_code = 480001      # Pincode to check
days = 7     # Number of days to check (starting from today)
min_age_limit = 18

# There is a rate limit of 100 queries per 5 min on the website.
attempts_per_minute = 1   # Number of attempts in one minute for all days                         

#-------------------------------------------------------------------
import os
import requests
import datetime
import time 
from sys import platform

alert_message = "Vaccine slots available for minimum age limit " + str(min_age_limit)

alert_command = ""
if platform == "win32" :     #windows
    alert_command = "PowerShell -Command \"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('" + alert_message  + "');\"" 
elif platform == "darwin" :      # OS X (mac)
    alert_command = "say " + alert_message

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

dateList = []
today = datetime.date.today()
for i in range(days):
    dateList.append( (today + datetime.timedelta(days=i)).strftime('%d-%m-%Y')  )

attempt = 1
while True:
    print ("Checking for available slots: Attempt " + str(attempt))
    for date in dateList:
        PARAMS = {'pincode':pin_code, 'date':date}
        try:
            r = requests.get(url = url,params=PARAMS, headers=headers)
            responses = r.json()
            for data in responses['sessions']:
                if (int(data['min_age_limit']) == min_age_limit):
                    print("-----------" + date + "-----------")
                    print("Center: " + data['name'])
                    print("Min Age Limit: " + str(data['min_age_limit']))
                    print("Available Capacity: " + str(data['available_capacity']))
                    print("Slots: " + str(data['slots']))
                    print()
                    os.system(alert_command)
        except Exception as e:
            print("ERROR:" + str(e))
            continue
    
    attempt += 1
    time.sleep(int(60/attempts_per_minute))


