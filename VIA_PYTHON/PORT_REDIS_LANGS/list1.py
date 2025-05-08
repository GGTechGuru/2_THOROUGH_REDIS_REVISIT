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
def list_try_a():
    r = rconn_global

    r.delete("fruits")

    r.lpush("fruits", "apple", "banana", "orange")

    r.rpush("fruits", "pear", "pomegranate", "tamarind")

    fruits = r.lrange("fruits", 0, -1)
    for index in range(0, r.llen("fruits")):
        fruits[index] = fruits[index].decode("utf-8")
        print(fruits[index])

##########################
if __name__ == "__main__":
    list_try_a()
