#!/bin/python

import subprocess
import time
import sys
import curses

import SlurmCliHelper


###
#
#   Small helper tool to visualize my running SLURM jobs
#
#####
def GetByStatus(lines, statusSearch):
    res = []
    for i in range(1, len(lines)):
        cur = lines[i]
        s = cur.split()
        if (len(s) > 7):
            id = s[0]
            partition = s[1]
            jobName = s[2]
            user = s[3]
            status = s[4]
            if status == statusSearch:
                res.append(cur)
    return res


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


def out(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def GetUsedNodes(input):
    seperated = input.split()
    filtered = []
    for i in range(0, len(seperated)):
        if (seperated[i].startswith("node")):
            filtered.append(seperated[i])
    numbers = []
    for i in range(0, len(filtered)):
        nodesOfJob = SlurmCliHelper.Job.parseNodeList(filtered[i])
        for n in nodesOfJob:
            numbers.append(n)
    numbers.sort()
    return numbers


def printChecked(stdscr, y, x, text, attrb=None):
    height, width = stdscr.getmaxyx()
    if (y > height):
        return
    if (x > width):
        return
    toMuch = (x + len(text)) - width
    if (toMuch > 0):
        text = text[:-toMuch]

    try:
        if (attrb is None):
            stdscr.addstr(y, x, text)
        else:
            stdscr.addstr(y, x, text, attrb)
    except:
        return


def main(stdscr):
    userName = "USERNAME"
    userNameParameter = "--user=" + userName

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
            stdscr.erase()
            curY = 0
            try:
                fullOutput = subprocess.check_output(['squeue', userNameParameter])
                usedNodes = GetUsedNodes(subprocess.check_output(['squeue']))
            except:
                printChecked(stdscr, curY, x, "Error calling squeue", curses.color_pair(curses.COLOR_RED))
                stdscr.refresh()
                time.sleep(1)
                continue

            outputLines = fullOutput.split("\n")
            header = outputLines[0]

            printChecked(stdscr, 0, 0, time.ctime(), curses.A_BOLD)
            curY += 1

            lastNode = 114
            i = 0
            free = 0;
            for y in range(0, 12):
                for x in range(0, 10):
                    i += 1;
                    if (i > lastNode):
                        break

                    if i in usedNodes:
                        printChecked(stdscr, curY, x, "#", curses.color_pair(curses.COLOR_RED))
                    else:
                        printChecked(stdscr, curY, x, "F", curses.color_pair(curses.COLOR_GREEN))
                        free += 1;

                curY += 1
            printChecked(stdscr, curY, 1, "Free Nodes: " + str(free), curses.A_BOLD)

            curY += 2

            if (len(outputLines) > 1):
                runningJobs = GetByStatus(outputLines, "R")
                pendingJobs = GetByStatus(outputLines, "PD")
                overviewString = str(str(len(runningJobs)) + " Jobs Running " + str(len(pendingJobs)) + " Jobs Pending")
                printChecked(stdscr, curY, 3, overviewString, curses.A_BOLD)
                curY += 1

                printChecked(stdscr, curY, 1, header, curses.A_BOLD)
                curY += 1

                for i in range(0, len(runningJobs)):
                    printChecked(stdscr, curY, 1, runningJobs[i])
                    curY += 1
                curY += 1

                for i in range(0, len(pendingJobs)):
                    printChecked(stdscr, curY, 1, pendingJobs[i])
                    curY += 1

            stdscr.refresh()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    return


curses.wrapper(main)
