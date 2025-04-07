#! /usr/bin/python3

import redis

def hash_try_a():
    r = redis.Redis()

    r.hset("user:1", "name", "Alice")

    r.hset("user:1", "age", 25)

    u_name = r.hget("user:1", "name").decode("utf-8")
    u_age = r.hget("user:1", "age").decode("utf-8")

    print("User: {0} Age: {1}".format(u_name, u_age))

##########################
if __name__ == "__main__":
    hash_try_a()
