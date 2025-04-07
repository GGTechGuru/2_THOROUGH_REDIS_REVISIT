#! /usr/bin/python3

import redis

import os
import time

import datetime

import calendar

import time


def set_conn():
    tp_str = os.getenv("REDIS_TEST_PORT")
    if tp_str is not None:
        test_port=int(tp_str)
        r = redis.Redis(test_port)
    else:
        r = redis.Redis()

    return r

################################

rconn_global = set_conn()

################################

def sync_try_a():

    r = rconn_global
    sleep_sec = 10

    some_key = str(time.time())

    status = r.set(some_key, "aval")

    # rval = r.sync().decode("utf-8")
    rval = r.sync()

    print("Return from sync():{0}".format(str(rval)))

##############################################################################################

if __name__ == "__main__":

    sync_try_a()


