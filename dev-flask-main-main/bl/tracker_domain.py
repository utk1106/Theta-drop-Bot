
# Importing libraries
import os
import smtplib, ssl
import struct
import time
import hashlib
from urllib.request import urlopen, Request
import urllib.request

import requests
# import requests as rq
import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from pytz import timezone
import config
from cryptography.fernet import Fernet


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url="https://time.is/"
# req = Request(
# url,
#     data=None,
#       headers={
#           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) >AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#           })
# try:
#     f = urlopen(req)
# except Exception as err:
#     print(err)
# print('complete')

# url = Request('https://www.thetadrop.com', data= None,
#               headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) >AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
# response = urlopen(url)
# headers = {}
# headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686)"
# req = urllib.request.Request(url)

# req = rq.get(url = 'https://thetadrop.com/drops')
# print('here')

hdr = {'User-Agent': 'Mozilla/5.0'}
hd = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

req = urllib.request.Request('https://www.thetadrop.com/drops',  headers=hdr)
response = urlopen(req).read()

# with urllib.request.urlopen(req) as response:
#    the_page = response.read()
ur = 'https://www.thetadrop.com/marketplace'
url = requests.get(ur,
              headers=headers)
response = urlopen(url).read()



executors = {'default': ThreadPoolExecutor(5), 'processpool': ProcessPoolExecutor(max_workers=3)}
scheduler = BackgroundScheduler(executors=executors, timezone=timezone('Asia/Kolkata'))
scheduler.start()


def send_Notifiation_email():
    receiver_email = ["thaokarutkarsh@gmail.com"]
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "thaokarutkarsh@gmail.com"




    password = ((decryption_token).decode('utf-8'))
    message = """
    Subject: Hi there
    
    Changes has taken place in Theta drop. Please Check. the given website.
    'https://www.thetadrop.com/'."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# send_Notifiation_email()

def check_for_changes_in_website(scheduler_object):
    if config.check_for_scheduler_status == 'RUN':
        try:
            response = urlopen(url).read()

            currentHash = hashlib.sha224(response).hexdigest()
            print('current hash 55', currentHash)

            time.sleep(5)

            response = urlopen(url).read()

            newHash = hashlib.sha224(response).hexdigest()
            print(' newHash 64', newHash)


            if newHash == currentHash:
                print('No changes')

            else:
                # send_Notifiation_email()
                print("something changed")

        except Exception as e:
            print("Error in check_for_changes_in_website function : ", e)


def schedule():
    print("HEERE")
    if config.check_for_scheduler_status != 'RUN':
        print("Stopped")
        scheduler.remove_all_jobs()
    elif config.check_for_scheduler_status == 'RUN':
        print("Running")
        for let in scheduler.get_jobs():
            print(let)
        scheduler.add_job(check_for_changes_in_website, "interval", seconds=10, args=[scheduler], coalesce=True,
                                replace_existing=True,
                                max_instances=1, id='check_for_changes_in_website')
