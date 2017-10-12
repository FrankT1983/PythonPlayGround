
import subprocess

class Job:
    def __init__(self, text):
        l = len(text)
        text =text.replace("  ", " ")
        while (len(text) != l):
            l = len(text)
            text = text.replace("  ", " ")

        parts = text.split(" ");

        self.valid = False

        current = 0;
        self.jobId , current , succsess = Job.NextInt(current, parts)
        if not succsess :
            return

        self.partition, current, succsess = Job.NextString(current, parts)
        if not succsess:
            return

        self.command, current, succsess = Job.NextString(current, parts)
        if not succsess:
            return

        self.user, current, succsess = Job.NextString(current, parts)
        if not succsess:
            return

        self.status, current, succsess = Job.NextString(current, parts)
        if not succsess:
            return

        self.runtime, current, succsess = Job.NextString(current, parts)
        if not succsess:
            return

        self.nodes, current, succsess = Job.NextInt(current, parts)
        if not succsess:
            return

        # problem with " (ReqNodeNotAvail, UnavailableNodes:) "
        self.nodeList, current, succsess = Job.NextString(current, parts)
        self.nodeList = self.nodeList.replace("(", "")
        if not succsess:
            return

        self.intNodeList = Job.parseNodeList(self.nodeList)

        self.valid = True
        return

    def __str__(self):
        return str(self.jobId) + " " + self.command + " " + self.user  + " " + str(self.nodes)  + " " + self.nodeList


    @staticmethod
    def NextInt(current, parts) :
        while current < len(parts) :
            try:
                result = int(parts[current])

                return result, current + 1, True
            except :
                current += 1
        return -1 , current , False

    @staticmethod
    def NextString(current, parts):
        while current < len(parts):
            tmp = str(parts[current]).strip()
            if (len(tmp) > 0) :
                return tmp, current + 1, True
            else:
                current += 1
        return -1, current, False

    @staticmethod
    def parseNodeList(text):
        result = []
        cur = text.replace("node", "").strip()
        if (str(cur).startswith("[")):
            # range
            cur = cur.replace("[", "")
            cur = cur.replace("]", "")
            ranges = cur.split(",")
            for r in range(0, len(ranges)):
                parts = ranges[r].split("-")
                if (len(parts) == 1):
                    try:
                        result.append(int(parts[0]))
                    except:
                        print("could convert" + str(parts))
                else:
                    if (len(parts) == 2):
                        start = int(parts[0])
                        end = int(parts[1])
                        for p in range(start, end+1):
                            result.append(p)
                    else:
                        print("could not get range " + str(cur))
        else:
            result.append(int(cur))

        return result


import re
class SCH:
    def GetFullQueueInfo(self):
        return subprocess.check_output(['squeue'])

    def GetJobsInQueue(self, text):
        if text is None:
            text = self.GetFullQueueInfo()

        jobs = []
        lines = text.split("\n")
        for line in lines:
            if "JOBID" in line:
                continue
            tmp = Job(line)
            if tmp.valid:
                jobs.append(tmp)
        return jobs

    def GetJobIdsInQueue(self, text):
        if text is None:
            text = self.GetFullQueueInfo()

        result = []
        jobs = self.GetJobsInQueue(text)
        for job in jobs :
            result.append(job.jobId)
        return result

    def QueueJobs(self, command):
        output = subprocess.check_output([command])
        return self.GetJobIdsFromSBatchOutput(output)

    def GetJobIdsFromSBatchOutput(self, text):
        regex = r"batch job (?P<id>[0-9]\w+)"
        m = re.findall(regex, text)
        result = []
        for match in m :
            try:
                result.append(int(match))
            except:
                continue
        return result
