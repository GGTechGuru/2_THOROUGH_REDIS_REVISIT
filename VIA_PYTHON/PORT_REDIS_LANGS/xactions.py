#! /usr/bin/python3

import redis

import multiprocessing

import math

import os

import time

####################################

# rconn_global = redis.Redis()

def set_conn():

    addr = os.getenv("REDIS_SINGLE_ADDR")

    if addr is not None:
        addr_as_list = addr.split(":")
        ip = addr_as_list[0]
        port = int(addr_as_list[1])
        r = redis.Redis(host=ip, port=port)

    else:
        print("REDIS_SINGLE_ADDR env not set. Using redis default")
        r = redis.Redis()

    return r

################################

rconn_global = set_conn()

################################

cond_global = multiprocessing.Condition()

####################################

def xactions_try_a(startx, endx, stagger):

    print("startx:{0}, endx:{1}".format(startx, endx))

    r = rconn_global

    pl = r.pipeline(transaction=True)

    for index in range(startx, endx):
        pl.rpush("akey", index)

    time.sleep(stagger)
    cond_global.acquire(timeout=20)
    cond_global.release()
    print("Completed stagger/sleep: {0}".format(str(stagger)))

    print("Beginning pipeline execute with startx:{0} @ t:{1}".format(startx, str(time.time())))
    pl.execute()
    print("Completed pipeline execute with startx:{0} @ t:{1}".format(startx, str(time.time())))

########################

def xactions_check():

    r = rconn_global

    rlist = r.lrange("akey", 0, -1)

    for index in range(0, len(rlist)):
        rlist[index] = int(rlist[index])

    for index in range(1, len(rlist)):
        if (rlist[index] < rlist[index-1]):
            print("List unordered at indices {0}-to-{1}".format(index-1, index))
            print("Values {0}-to-{1}".format(rlist[index-1], rlist[index]))

##########################

def pl_test_mon_try_a():

    r = rconn_global
    r.delete("akey")

    processes = []

    stagger_sec = 0.2

    interval = 200000
    for i in range(0, 3):
        startx = i * interval
        endx = (i + 1) * interval
        stagger = i * stagger_sec

        print("startx:{0}, endx:{1}".format(startx, endx))

        p = multiprocessing.Process(target=xactions_try_a, args=(startx, endx, stagger))
        processes.append(p)

    with cond_global:
        cond_global.notify_all()

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    xactions_check()
##########################

def xactions_discard_try_c():

    r = rconn_global

    some_key = "akey_" + str(time.time()).split(".")[-1]

    pl = r.pipeline(transaction=True)

    for index in range(0,10):
        pl.rpush(some_key, index)

    pl.discard()

    pl = r.pipeline(transaction=True)
    for index in range(11,20):
        pl.rpush(some_key, index)

    pl.execute()

    l = list(r.lrange(some_key, 0, -1))
    l.sort()

    print("List after discarding pipeline push:{0}-{1}, adding push:{2}-{3}::\n{4}".format(0, 10-1, 11, 20-1, str(l)))
    

########################

if __name__ == "__main__":

    # pl_test_mon_try_a()

    xactions_discard_try_c()
