from workers import celery
from datetime import datetime
from mail import *


@celery.task()
def sayHello(name):
    print("INSIDE TASK")
    print("Hello {}".format(name))
    return "Hello {}".format(name)

@celery.task()
def csv():
    res = send_email("h@h.com","Subject","message")
    return res