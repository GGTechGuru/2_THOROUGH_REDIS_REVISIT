#! /usr/bin/python3

import redis

def list_try_a():
    r = redis.Redis()

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
