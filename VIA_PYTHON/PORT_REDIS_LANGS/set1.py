#! /usr/bin/python3

import redis
import os

import random
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
def set_try_a():

    r = rconn_global

    r.delete("tags")

    r.sadd("tags", "java", "redis", "programming")
    r.sadd("tags", "one_more_member")

    tags = r.smembers("tags")

    print(str(tags))

    r.srem("tags", "java")
    r.sadd("tags", "python")

    tags = r.smembers("tags")

    for mem in tags:
        tags.remove(mem)
        tags.add(mem.decode("utf-8"))

    print(str(tags))

    print("Is 'java' a 'tags' set member:{0}".format(r.sismember("tags", "java")))
    print("Is 'python' a 'tags' set member:{0}".format(r.sismember("tags", "python")))

##########################


def sinter_try_b():

    r = rconn_global

    r.delete('rag1')
    r.delete('rag2')
    r.delete('rag4')

    for count in range(0,20):
        which_set = random.randint(1, 1|(1<<1)|(1<<2))

        some_val = str(time.time()).split(".")[-1]
        if which_set & (1<<0):
            key = "rag1"
            rval = r.sadd(key, some_val)
            # print("rval from sadd( {0}, {1} ):{1}".format( key, some_val, str(rval)))

        if which_set & (1<<1):
            key = "rag2"
            rval = r.sadd(key, some_val)


        if which_set & (1<<2):
            key = "rag4"
            rval = r.sadd(key, some_val)


    s1 = list(r.smembers('rag1'))
    s1.sort()
    print("smembers('rag1'):{0}".format(str(s1)))

    s2 = list(r.smembers('rag2'))
    s2.sort()
    print("smembers('rag2'):{0}".format(str(s2)))

    s4 = list(r.smembers('rag4'))
    s4.sort()
    print("smembers('rag4'):{0}".format(str(s4)))


    s1_2_4 = list(r.sinter('rag1', 'rag2', 'rag4'))
    s1_2_4.sort()
    print("sinter('rag1', 'rag2', 'rag4'):{0}".format(str(s1_2_4)))
    
    py_s1 = set(s1)
    py_s2 = set(s2)
    py_s4 = set(s4)

    py_inter = py_s1 & py_s2 & py_s4
    py_inter_l = list(py_inter)
    py_inter_l.sort()
    print("Expected intersection via python set op:{0}".format(str(py_inter_l)))

###########################

if __name__ == "__main__":
    # set_try_a()

    sinter_try_b()
