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

def genops_try_a():

    r = rconn_global

    r.delete("newkey")
    print("Does 'newkey' exist after delete:{0}\n".format(r.exists('newkey')))

    r.set("newkey", "someval")
    print("Does 'newkey' exist after set:{0}\n".format(r.exists('newkey')))

##########################

def type_try_b():
    r = rconn_global

    key = "str_key"
    r.delete(key)
    r.set(key, "some_str")
    rval = r.type(key).decode("utf-8")
    print("Key:{0} has redis type:{1}".format(key, str(rval)))

    key="set_key"
    r.delete(key)
    r.sadd(key, "v1", "v2")
    rval = r.type(key).decode("utf-8")
    print("Key:{0} has redis type:{1}".format(key, str(rval)))

    key="hash_key"
    r.delete(key)
    r.hset(key, "hash1", "val1")
    r.hset(key, "hash2", "val2")
    rval = r.type(key).decode("utf-8")
    print("Key:{0} has redis type:{1}".format(key, str(rval)))

    key="z_key"
    op = {
        "k1":1000,
        "k2":10,
        "k3":100000,
    }
    r.delete(key)
    r.zadd(key, op)
    rval = r.type(key).decode("utf-8")
    print("Key:{0} has redis type:{1}".format(key, str(rval)))

    
    
##########################

def config_get_try_c():

    r = rconn_global

    r.set("newkey", "someval")
    print("Does 'newkey' exist after set:{0}\n".format(r.exists('newkey')))

    rval = r.config_get()
    print("config_get():{0}\n".format(str(rval)))

##########################

def debug_object_try_e():

    r = rconn_global

    rval = r.config_get("enable-debug-command")
    print("config_get(enable-debug-command) returned::{0}".format(str(rval)))
    print("type of return from config_get(enable-debug-command) returned::{0}".format(str(type(rval))))

    if (rval["enable-debug-command"] is None) or (rval["enable-debug-command"] != "local"):
        print("Config 'enable-debug-command' to 'local' & restart redis");
        return

    r.set("newkey", "someval")
    rval = r.debug_object("newkey")
    print('debug_object("newkey") returned::{0}'.format(str(rval)))

##########################

def command_get_try_g():

    r = rconn_global

    r.set("newkey", "someval")

    rval = r.command()
    print("type of return from command():{0}\n".format(str(type(rval))))

    keys = list(rval.keys())
    keys.sort()
    print("List of keys from command():{0}\n".format(str(keys)))
    

##########################
if __name__ == "__main__":
    # type_try_b()

    # config_get_try_c()

    # debug_object_try_e()

    command_get_try_g()
