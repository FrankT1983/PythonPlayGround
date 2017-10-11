#!/usr/bin/python

try:
    import urllib.request
except:
    from six.moves import urllib
from bs4 import BeautifulSoup

import time
import  datetime

def GetAllPledgeLevels(url) :
    f = urllib.request.urlopen(url)
    if f is None :
        return  None
    html= f.read()
    f.close()

    if html is None :
        return  None

    soup = BeautifulSoup(html , "lxml")
    pledges = soup.find_all("div", class_="pledge__info")
    if pledges is None :
        return  []

    all_Pledgeds = []
    for p in pledges:
        title = p.find("h3", class_="pledge__title")
        limit = p.find("span", class_="pledge__limit")

        if not title is None :
            pledgeName = title.text.strip()
            pledgeLimit = ""
            if not limit is None:
                pledgeLimit = limit.text.strip()

            all_Pledgeds.append([pledgeName,pledgeLimit])

    timeLeft = soup.find_all("div", class_="ksr_page_timer")
    endTime = ""
    if (not timeLeft is None):
        for time in timeLeft :
            if "data-end_time" in time.attrs :
                endTime = time.attrs["data-end_time"]
    format = "%Y-%m-%dT%H:%M:%S"
    withoutTimeZone =str(endTime).replace("-04:00","")
    withoutTimeZone = withoutTimeZone.replace("-05:00", "")
    asDate = datetime.datetime.strptime(withoutTimeZone,format)
    delta = asDate  - datetime.datetime.now()   # not precise, time zones seem non trivial in python

    return all_Pledgeds , delta


def GetLongesPledgeName(p_array) :
    if p_array is None : return -1

    res = len(p_array[0][0])
    for pledge in p_array :
        res = max(res,len(pledge[0]))

    return res


def PrintToConsole(projects):
    for p in projects :
        print(str(p[0]) + "\t\tremaining\t" + str(p[2]) )

        longestName= GetLongesPledgeName(p[1])
        for pledge in p[1] :
            print("\t" + str(pledge[0]).ljust(longestName) + "\t" + str(pledge[1]))
        print("\n")


def PrintChecked(stdscr,y,x,text, attrb = None):
    height, width = stdscr.getmaxyx()
    if (y > height):
        return
    if (x > width):
        return
    toMuch = (x +len(text)) - width
    if (toMuch > 0):
        text = text[:-toMuch]

    try:
        if(attrb is None):
            stdscr.addstr(y, x, text)
        else:
            stdscr.addstr(y, x, text, attrb)
    except:
        return

def PrintAttributeFromPledgeString(string):
    if ("no longer available" in string) :
        return curses.color_pair(curses.COLOR_RED)
    if ("left" in string):
        return curses.color_pair(curses.COLOR_GREEN)



def PrintCurses(projects, stdscr) :
    stdscr.erase()
    curY = 0

    for p in projects :
        PrintChecked(stdscr,curY,2,str(p[0]) + "\t\tremaining\t" + str(p[2]) )
        curY +=1

        longestName= GetLongesPledgeName(p[1])
        for pledge in p[1] :
            PrintChecked(stdscr, curY, 4,               str(pledge[0]))

            attr= PrintAttributeFromPledgeString(pledge[1])
            PrintChecked(stdscr, curY, 4+longestName+4, str(pledge[1]),attr)
            curY += 1

        curY += 1
    curY += 1

    PrintChecked(stdscr, curY, 5, "Last Checked: " + str(datetime.datetime.now()))
    stdscr.refresh()



def main(stdscr):

    refreshInterval = 60

    try:
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)

        curses.init_pair(curses.COLOR_RED,
                         curses.COLOR_RED,
                         curses.COLOR_BLACK)
        curses.init_pair(curses.COLOR_GREEN,
                         curses.COLOR_GREEN,
                         curses.COLOR_BLACK)

        while True:
            PrintCurses(GetParsedProjects(), stdscr)
            time.sleep(refreshInterval)

    except KeyboardInterrupt:
        pass
    return


def GetParsedProjects() :
    projects = []
    for proj in toWatch:
        pledges, delta = GetAllPledgeLevels(proj[1])
        projects.append([proj[0], pledges, delta])
    return projects

def RunOnceForTest():
    PrintToConsole(GetParsedProjects())


toWatch = [
    ["CubiOne", "https://www.kickstarter.com/projects/99671519/cubibot-the-new-standard-of-modern-consumer-3d-pri"],
    ["Tsukuyumi", "https://www.kickstarter.com/projects/kingracoongames/tsukuyumi-full-moon-down-a-strategic-board-game"]
]


try :
    import curses   # does not work under windows
    curses.wrapper(main)
except:
    RunOnceForTest()


