#! /usr/bin/python3

import redis

import os

rconn_global = redis.Redis()

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


