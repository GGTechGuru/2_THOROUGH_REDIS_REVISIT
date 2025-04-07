#! /usr/bin/python3

import redis

import os
import time

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

def save_ops_try_a():

    r = rconn_global
    status = r.set("akey", "aval")
    rval = r.bgsave()
    print("Return from bgsave:{0}".format(str(rval)))

    try:
        rval = r.save()
        print("Return from save:{0}".format(str(rval)))
    except Exception as e:
        print("Call to save() got exception message:{0}".format(str(e.args[0])))


########################

def bgrewriteaof_try_b():

    r = rconn_global
    status = r.set("bkey", "bval")

    try:
        rval = r.bgrewriteaof()
        print("Return from bgrewriteaof:{0}".format(str(rval)))
    except Exception as e:
        print("Call to bgrewriteaof() got exception message:{0}".format(str(e.args[0])))

##############################################################################################

if __name__ == "__main__":

    bgrewriteaof_try_b()


