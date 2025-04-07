#! /usr/bin/python3

import redis

import os
import time

rconn_global = redis.Redis()

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


