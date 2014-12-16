# -*- coding: utf-8 -*-
import time


def test_create():
    f = open("applications/MiniTimeMK/views/default/index_generated.html", 'w')
    f.write("Testing Dynamic page generation")
    posts = []

    f.close()


def testf():
    t = time.ctime()
    open('/tmp/sch_testing', 'a').write('Testing 1 2 3' + t + '\n')
    print("HELLO NIGGERS")
    print(t)
    return t

from gluon.scheduler import Scheduler
Scheduler(db, dict(testtask=testf))
