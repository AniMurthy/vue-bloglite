from workers import celery
from datetime import datetime


@celery.task()
def sayHello(name):
    print("INSIDE TASK")
    print("Hello {}".format(name))
    return "Hello {}".format(name)