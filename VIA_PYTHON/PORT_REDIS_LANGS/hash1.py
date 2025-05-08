#! /usr/bin/python3

import redis

import os


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

def hash_try_a():

    r = rconn_global

    r.hset("user:1", "name", "Alice")

    r.hset("user:1", "age", 25)

    u_name = r.hget("user:1", "name").decode("utf-8")
    u_age = r.hget("user:1", "age").decode("utf-8")
    print("User: {0} Age: {1}".format(u_name, u_age))

    u_all = r.hgetall("user:1")
    print("Return from hgetall()::\n{0}".format(str(u_all)))


##########################
def hmset_try_b():

    r = rconn_global

    kv = {"name":"Anita", "age":18}

    r.hmset("user:2", kv)

    u_name = r.hget("user:2", "name").decode("utf-8")
    u_age = r.hget("user:2", "age").decode("utf-8")
    print("User: {0} Age: {1}".format(u_name, u_age))

    u_all = r.hgetall("user:2")
    print("Return from hgetall()::\n{0}".format(str(u_all)))


##########################

if __name__ == "__main__":
    # hash_try_a()

    hmset_try_b()
