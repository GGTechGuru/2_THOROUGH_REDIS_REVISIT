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
def key_type_try(exp_sec=30):

    r = rconn_global

#    tp_str = os.getenv("REDIS_TEST_PORT")
#    if tp_str is not None:
#        test_port=int(tp_str)
#        r = redis.Redis(test_port)
#    else:
#        r = redis.Redis()
#
    set_val = "aval"

    status = r.set("str_key", set_val)
    type_rval = r.type("str_key")
    print("Return from key type check for basic key-val pair is {0}".format(type_rval))

    got_val = r.get("str_key").decode("utf-8")
    print("Actual set value {0} vs returned {1}".format(set_val, got_val))

    set_val = 127
    status = r.set("int_key", set_val)
    got_val = r.get("int_key").decode("utf-8")
    print("Actual set value {0} vs returned {1}".format(set_val, got_val))

    type_rval = r.type("int_key")
    print("Return from key type check for int key-val pair is {0}".format(type_rval))

    type_rval = r.type("not_a_key")
    print("Return from key type check for non-existent is {0}".format(type_rval))


##############################################################################################

if __name__ == "__main__":

    key_type_try()


