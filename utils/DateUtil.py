import time
from datetime import datetime
from datetime import timedelta

now = datetime.now()


def getfulldate():
    return now.strftime("%Y-%m-%d")

def gethour():
    return now.strftime("%H")

def getmin():
    return now.strftime("%M")

def convertDate(dt):
    return datetime.strptime(dt, '%b%d%Y').strftime('%Y-%m-%d')

def getPastDate(days):
    thepast = now - timedelta(days=days)
    return thepast.strftime("%Y-%m-%d")

def getFutureDate(days):
    future = now + timedelta(days=days)
    return future.strftime("%Y-%m-%d")