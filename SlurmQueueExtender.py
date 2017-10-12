#!/usr/bin/python

# my Slurm Queue is to small to queue all my 10000 short running jobs at once, and I don't want to get up in the
# middle of the night
# -> write small tool


import sys
import pickle
import json
import time

import SlurmCliHelper
import datetime


# constants
jobFile = "jobs.pickle"
refreshInterval = 60



if ("create" in sys.argv) :
    # simple way to create job file
    toExecute = [
        ["./script1", 100],
        ["./script2", 100],
        ["./script3", 100]
    ]

    with open(jobFile, 'w') as outfile:
        json.dump(toExecute, outfile)


if ("runJobs" in sys.argv) :
    print("Start Running Jobs")
    helper = SlurmCliHelper.SCH()
    toExecute = []
    with open(jobFile) as infile:
        toExecute = json.load(infile)

    myJobsInQueue = []

    try:
        while True :
            # check what is still running
            if (len(myJobsInQueue) > 0 ):
                jobString = helper.GetFullQueueInfo()
                jobsInQueue = helper.GetJobIdsInQueue(jobString)

                stillInQueue = []
                for job in myJobsInQueue :
                    if job in jobsInQueue :
                        stillInQueue.append(job)
                myJobsInQueue = stillInQueue
                print(str(datetime.datetime.now()) + " : Still " + str(len(myJobsInQueue)) + " jobs in queue")
            else :
                #start next thing
                startJob = None
                for job in toExecute :
                    if job is None:
                        continue
                    if len(job) <2 :
                        continue
                    remaining = 0
                    try :
                        remaining = int(job[1])
                    except:
                        remaining = -1
                    if remaining <1 :
                        continue

                    startJob = job
                    job[1] = remaining - 1

                    # update job file
                    with open(jobFile, 'w') as outfile:
                        json.dump(toExecute, outfile)
                    break

                if startJob is None :
                    print("Nothing left to do")
                    quit(0)

                print("Start new script " + startJob[0])
                startedJobIds = helper.QueueJobs(startJob[0])
                print("Started :" + str(startedJobIds))

                for id in startedJobIds :
                    myJobsInQueue.append(id)

            time.sleep(refreshInterval)
    except KeyboardInterrupt:
        print("Quit, Jobs remaining in Queue :" + str(myJobsInQueue))
        print("For deleting:")
        for job in myJobsInQueue :
            print("scancel " + str(job))
