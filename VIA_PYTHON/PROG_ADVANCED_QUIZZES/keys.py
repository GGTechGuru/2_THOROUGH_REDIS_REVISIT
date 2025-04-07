#! /usr/bin/python3

import redis

import os

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

def keys_try_a():

    r = rconn_global

    set_val = "aval"

    status = r.set("str_key", set_val)

    set_val = 127
    status = r.set("int_key", set_val)
    
    rval = r.keys()

    rutf = []
    # for el in rval:
        # rutf.append(el.decode("utf-8"))

    rutf = list(map(lambda x: x.decode("utf-8"), rval))

    print("Return from r.keys:{0}".format(str(rval)))
    print("Return from r.keys:{0}".format(str(rutf)))


##############################################################################################

if __name__ == "__main__":

    keys_try_a()


