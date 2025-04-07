#! /usr/bin/python3

import redis

import os
import time

import datetime

import calendar

import time


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


