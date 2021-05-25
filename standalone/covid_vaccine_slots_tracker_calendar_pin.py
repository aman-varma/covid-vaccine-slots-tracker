#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Aman Varma     amanvarma993@gmail.com
"""
#----------------------- Parameters to change ----------------------

pin_codes = [480001, 560023, 560029, 560036]      # Pincodes to check
min_age_limit = 18
num_alerts = 5    # Number of alert messages
dose = "1"        # for dose 2 use "2"
# There is a rate limit of 100 queries per 5 min on the website.
attempts_per_minute = 5   # Number of attempts in one minute for all days                         
#-------------------------------------------------------------------
import os
import requests
import datetime
import time 
from sys import platform


url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

attempt = 1
while True:
    today = datetime.date.today().strftime('%d-%m-%Y')
    print ("Checking for available slots: Attempt " + str(attempt))
    available_pin_codes = []
    for pin_code in pin_codes:
        PARAMS = {'pincode':pin_code, 'date':today}
        try:
            r = requests.get(url = url,params=PARAMS, headers=headers)
            responses = r.json()
            for centers in responses['centers']:
                for data in centers['sessions']:
                    if (int(data['min_age_limit']) == min_age_limit and int(data['available_capacity_dose' + dose]) > 0):
                        print("----------- date: " + data['date'] + " ----------- pin code: " + str(pin_code) + " -----------")
                        print("Center: " + centers['name'])
                        print("Min Age Limit: " + str(data['min_age_limit']))
                        print("Available Capacity: " + str(data['available_capacity_dose' + dose]) + "  ,Dose: " + dose)
                        print("Slots: " + str(data['slots']))
                        print()
                        if pin_code not in available_pin_codes:
                            available_pin_codes.append(pin_code)
        except Exception as e:
            print("ERROR:" + str(e))
            continue
   
    attempt += 1
    if len(available_pin_codes) != 0:
        alert_message = "Vaccine slots available for minimum age limit " + str(min_age_limit)
        alert_message = alert_message + ", for pin codes: "
        for pin_code in available_pin_codes:
            alert_message = alert_message + " ".join(str(pin_code)) + ", " 

        alert_command = ""
        if platform == "win32" :     #windows
            alert_command = "PowerShell -Command \"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('" + alert_message  + "');\"" 
        elif platform == "darwin" :      # OS X (mac)
            alert_command = "say " + alert_message

        print(alert_message)
        for x in range(num_alerts):
            os.system(alert_command)

    else:  
        time.sleep(int(60/attempts_per_minute))


