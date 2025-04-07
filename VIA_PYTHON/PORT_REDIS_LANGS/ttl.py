#! /usr/bin/python3

import redis

import os
import time

import datetime

import calendar

def ttl_try_a(exp_sec=30):

    r = None
    sleep_sec = 10

    tp_str = os.getenv("REDIS_TEST_PORT")
    if tp_str is not None:
        test_port=int(tp_str)
        r = redis.Redis(host='localhost', port=7000, db=0)
    else:
        r = redis.Redis()

    status = r.set("akey", "aval")
    ttl = r.ttl("akey")
    print("Return from ttl check before key made expiring is {0}".format(ttl))

    ttl = r.ttl("no_key")
    print("Returned from ttl check for non-existent key is {0}".format(ttl))

    status = r.expire("akey", exp_sec)

    ttl = r.ttl("akey")
    print("Remaining ttl at call 1 is {0}".format(ttl))

    time.sleep(sleep_sec)
    ttl = r.ttl("akey")
    print("Remaining ttl at call after {1} more seconds is {0}".format(ttl, sleep_sec))

    time.sleep(sleep_sec)
    ttl = r.ttl("akey")
    print("Remaining ttl at call after {1} more seconds is {0}".format(ttl, sleep_sec))


##############################################################################################

def ttl_try_b(exp_sec=120):

    r = None
    sleep_sec = 10

    tp_str = os.getenv("REDIS_TEST_PORT")
    if tp_str is not None:
        test_port=int(tp_str)
        r = redis.Redis(test_port)
    else:
        r = redis.Redis()

    r.delete("akey")

    status = r.set("akey", "aval")
    ttl = r.ttl("akey")

    ttt = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_sec)

    print("Types: datetime.datetime.utcnow():{0}, datetime.timedelta():{1}".format(
        type(datetime.datetime.utcnow()),
        type(datetime.timedelta(seconds=exp_sec))))

    print("ttt=={0}, ttt.timetuple()=={1}".format(str(ttt), str(ttt.timetuple())))
    ts = calendar.timegm(ttt.timetuple())
    print("Types: calendar.timegm(ttt.timetuple()):{0}".format(type(calendar.timegm(ttt.timetuple()))))

    print("Calling expireat with UTC TS:{0}, which is {1} seconds ahead.".format(str(ts), exp_sec))
    status = r.expireat("akey", ts)

    ttl = r.ttl("akey")
    print("Remaining ttl at call 1 is {0}".format(ttl))

##############################################################################################

if __name__ == "__main__":

    ttl_try_a(120)


