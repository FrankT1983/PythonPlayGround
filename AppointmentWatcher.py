#!/usr/bin/python

try:
    import urllib.request
except:
    from six.moves import urllib
from bs4 import BeautifulSoup

import time
import  datetime











def GetAppointments() :
    html = None
    try:
        f = urllib.request.urlopen("https://netappoint.de/ot/stadtjena/index.php?company=stadtjena&cur_cause=0&step=2")
        if f is None:
            return None
        html = f.read()
        f.close()
    except :
        return  []

    if html is None:
        return []

    soup = BeautifulSoup(html, "lxml")
    dates = soup.find_all("a", class_="nat_calendar_weekday_bookable")
    if dates is None:
        return []

    allDates = []
    for p in dates:
#        spans = p.findAll("span")
#        if spans is None:
#            continue
#        for s in spans:
#            try:
#                day = int(s.contents[0])
#            except :
#                continue
        for bar in p.contents:
            try:
                day = int(bar)
                allDates.append(day)
            except :
                day = 100
    return allDates

def Alert(date):
    print("New available at " + str(date))

def RunOnceForTest():
    dates = GetAppointments()
    print( str(datetime.datetime.now()) + " : " +str(dates))
    for d in dates :
        if d < 25 :
            Alert(d)


refreshInterval = 20
RunOnceForTest()
while (True) :
    time.sleep(refreshInterval)
    RunOnceForTest()

