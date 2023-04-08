from workers import celery
from datetime import datetime
from mail import *
import os
import flask_excel as excel
import csv
from flask import current_app as app
import requests
from celery.schedules import crontab

# excel.init_excel(app)

@celery.task()
def downloadcsv(d1,file_name,email):
  if not os.path.exists('../data'):
    os.makedirs('../data')
  with open(file_name,'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(d1)
  print("CSV sent (in celery)")
  subject="CSV File"
  message="Please find your CSV File attached below.<br>This is an auto generated e-mail.<br>Please do not respond to this. "
  attachment_file=file_name
  res = send_email(email,subject,message,attachment_file)
  

@celery.task()
def pdf(email,file_name):
  if not os.path.exists('../data'):
    os.makedirs('../data')
  subject="PDF Report"
  message="Please find your PFD report attached below.<br>This is an auto generated e-mail.<br>Please do not respond to this. "
  attachment_file=file_name
  print("mail sent (in celery)")
  res = send_email(email,subject,message,attachment_file)

@celery.on_after_configure.connect
def daily_reminder(sender,**kwargs):
  sender.add_periodic_task(
        crontab(hour=15, minute=54, day_of_week="*"),
        daily_rem.s(),
        name='Daily Reminder'
         )

@celery.task()
def daily_rem():
  webhook_url='https://chat.googleapis.com/v1/spaces/AAAAtHhqwFk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Wz6d0LY7CZgqPUg-81xOUaIIkihPw5GKScsOiLgOo5E%3D'
  data = {'text':'Did you check the blog today?\nBe sure to check the blog for new posts!'}
  response = requests.post(webhook_url,json=data)
  print("message sent (in celery)")
  if response.status_code == 200:
    return "message sent succesfully"
  else:
    return "message not sent"


@celery.task()
def hello():
  print("hello from celery")