from workers import celery
from datetime import datetime
from mail import *
import os


@celery.task()
def sayHello(name):
    print("INSIDE TASK")
    print("Hello {}".format(name))
    return "Hello {}".format(name)

@celery.task()
def csv(email,file_name):
    subject="PDF Report"
    message="Please find your PFD report attached below.<br>This is an auto generated e-mail.<br>Please do not respond to this. "
    attachment_file=file_name
    res = send_email(email,subject,message,attachment_file)
    return res