from unittest import TestCase
from SlurmCliHelper import Job

class TestJob(TestCase):
    def test_parseNodeList_singleNode(self):
        singleNode = Job.parseNodeList(" node093")
        if not(len(singleNode) == 1) :
            self.fail()

        if not(singleNode[0] == 93) :
            self.fail()

    def test_parseNodeList_range(self):
        nodes = Job.parseNodeList(" node[070-073] ")
        if not(len(nodes) == 4) :
            self.fail()

        expected = [ 70,71,72,73]
        for e in expected:
            if not e in nodes:
                self.fail()

    def test_parseNodeList_multipleRanges(self):
        nodes = Job.parseNodeList("  node[001,007-008,019,110-111] ")
        if not(len(nodes) == 6) :
            self.fail()

        expected = [1,7,8,19,110,111]
        for e in expected:
            if not e in nodes:
                self.fail()


    def test_parseNodeList_WaitStates(self):
        nodes = Job.parseNodeList("  (Resources) ")
        if not(len(nodes) == 0) :
            self.fail()


