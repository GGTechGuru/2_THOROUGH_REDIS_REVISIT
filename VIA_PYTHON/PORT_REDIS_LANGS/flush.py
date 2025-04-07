#! /usr/bin/python3

import redis

import os
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

def flushdb_try_a():

    r = rconn_global
    some_key = str(time.time())
    status = r.set(some_key, "aval")
    
    rval = r.keys()
    print("Return from keys() before flushdb():{0}".format(str(rval)))

    rval = r.flushdb()
    print("Return from flushdb():{0}".format(str(rval)))

    rval = r.keys()
    print("Return from keys() after flushdb():{0}".format(str(rval)))

##############################################################################################

def flushall_try_b():

    r = rconn_global

    db_list = [0, 1, 2, 3, 4]

    for db in db_list:

        rval = r.select(db)

        some_key = str(time.time())
        status = r.set(some_key, "aval")
        
        rval = r.keys()
        print("DB#:{0} keys() before flushall():{1}".format(db, str(rval)))
    
    rval = r.flushall()
    print("Return from flushall():{0}".format(str(rval)))
    
    for db in db_list:

        rval = r.select(db)

        rval = r.keys()
        print("DB#:{0} keys() after flushall():{1}".format(db, str(rval)))

############################

if __name__ == "__main__":

    flushall_try_b()


