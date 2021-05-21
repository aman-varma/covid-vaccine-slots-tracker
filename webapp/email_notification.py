import smtplib, ssl
import certifi
import time

sender_email = "abc@example.com"
port = 465
password = "password"
wait_time = 30*60   # Time to wait before sending the mail again for the same pincode. 

g_message ="""\
Subject: Vaccine slots available for pin code: """

def create_message(pincode, content):
    message = g_message + str(pincode)
    message += "\n\n" + content
    return message

def send_mail(available_slots):
    context = ssl.create_default_context(cafile=certifi.where())
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("vaccineslottracker6@gmail.com", password)
        for pin_code in available_slots:
            
            receiver_mail_list = available_slots[pin_code][0]
            message = create_message(pin_code, available_slots[pin_code][1])
            for receiver_email in receiver_mail_list:
                print("-----Sending email to " + receiver_email + " for pin code: " + str(pin_code))
                server.sendmail(sender_email, receiver_email, message)

def notify(pin_code_email_mapping):
    available_slots = {}
    for key in pin_code_email_mapping:
        email, pin_code = decode_key(key)

        message = pin_code_email_mapping[key][0]
        last_mail_sent = time.time() - pin_code_email_mapping[key][1]
        slots_available = pin_code_email_mapping[key][2]
        email_registered = pin_code_email_mapping[key][3]
        if email_registered == True and slots_available == True and last_mail_sent > wait_time:
            pin_code_email_mapping[key][1] = time.time()
            if pin_code in available_slots:
                available_slots[pin_code][0].append(email)
            else:
                available_slots[pin_code] = [[email], message] 

    if len(available_slots) > 0:
        send_mail(available_slots)

def decode_key(key):
    email, pin_code = key.split(" ")
    return email, int(pin_code)

