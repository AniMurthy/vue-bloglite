from workers import celery
from datetime import datetime
from mail import *
import os
import flask_excel as excel
import csv
from flask import current_app as app

excel.init_excel(app)

@celery.task()
def csv(d1,file_name):
    with open(file_name,'w',newline='') as file:
      writer = csv.writer(file)
      writer.writerows(d1)

@celery.task()
def pdf(email,file_name):
    subject="PDF Report"
    message="Please find your PFD report attached below.<br>This is an auto generated e-mail.<br>Please do not respond to this. "
    attachment_file=file_name
    res = send_email(email,subject,message,attachment_file)
    return res