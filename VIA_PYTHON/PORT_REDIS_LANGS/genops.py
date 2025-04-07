#! /usr/bin/python3

import redis

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
if __name__ == "__main__":
    type_try_b()
