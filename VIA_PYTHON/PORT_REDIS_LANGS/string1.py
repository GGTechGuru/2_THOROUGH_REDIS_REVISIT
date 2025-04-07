#! /usr/bin/python3

import redis


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
def string_try_a():
    r = rconn_global

    r.set("name1", "Alice")
    r.set("age1", 25)

    name = r.get("name1").decode("utf-8")
    age = r.get("age1").decode("utf-8")

    print("User1: {0} Age1: {1}".format(name, age))

##########################

def setnx_try_b():
    r = rconn_global

    r.set("name1", "Alice")
    r.set("age1", 25)

    r.set("name2", "Cooper")
    r.set("age2", 11)

    name = r.get("name1").decode("utf-8")
    age = r.get("age1").decode("utf-8")
    print("Before set+setnx: User1: {0} Age1: {1}".format(name, age))
    name = r.get("name2").decode("utf-8")
    age = r.get("age2").decode("utf-8")
    print("Before set+setnx: User2: {0} Age2: {1}".format(name, age))

    r.set("name1", "Tricia")
    r.set("age1", 20)

    r.setnx("name2", "Maharajah")
    r.setnx("age2", 101)

    name = r.get("name1").decode("utf-8")
    age = r.get("age1").decode("utf-8")
    print("After set+setnx: User1: {0} Age1: {1}".format(name, age))
    name = r.get("name2").decode("utf-8")
    age = r.get("age2").decode("utf-8")
    print("After set+setnx: User2: {0} Age2: {1}".format(name, age))

##########################
if __name__ == "__main__":
    setnx_try_b()
