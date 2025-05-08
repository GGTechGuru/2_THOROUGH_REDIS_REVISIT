#! /usr/bin/python3

import redis

import os
import random
import time


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
def o_set_try_a():

    o_dict = {
        "PlayerOne":3000.0,
        "PlayerTwo":1500.0,
        "PlayerThree":8200.0
    }

    r = rconn_global

    r.zadd("o_key", o_dict)

    rval = r.zrange("o_key", 0, -1)
    print("Type from zrange:{0} ".format(type(rval)))
    print("Vals from zrange:{0} ".format(str(rval)))

    rval = r.zrevrange("o_key", 0, -1)
    print("Type from zrevrange:{0} ".format(type(rval)))
    print("Vals from zrevrange:{0} ".format(str(rval)))

    rval = r.zrank("o_key", "PlayerTwo")
    print("zrank o_key PlayerTwo:{0}".format(rval))

    rval = r.zrevrank("o_key", "PlayerTwo")
    print("zrevrank o_key PlayerTwo:{0}".format(rval))

    rval = r.zrevrank("o_key", "Non-player")
    print("zrevrank o_key Non-player:{0}".format(rval))

    rval = r.zrandmember("o_key")
    print("zrandmember('o_key') returned::{0}".format(str(rval)))

    rval = r.zrem("o_key", "PlayerThree");
    rval = r.zrevrange("o_key", 0, -1)
    print("After zrem({0}), return from zrevrange::\n{1} ".format("PlayerThree", str(rval)))


##########################

def zrangeby_try_b():

    o_dict = {}

    o_by_score = []
    o_by_name = []

    r = rconn_global

    for index in range(0, 50):
        hash_key = "Player_{0:02}".format(random.randint(0,30))
        score = random.randint(0,10)
        o_dict[hash_key] = score

    o_key = str(time.time()).split(".")[-1]

    for k in o_dict.keys():
        score = o_dict[k]
        o_by_score.append("{0:02}:{1}".format(score, str(k)))
        o_by_name.append("{0}:{1}".format(str(k), score))

    o_by_score.sort()
    o_by_name.sort()

    r.zadd(o_key, o_dict)

    ks = list(o_dict.keys())
    ks.sort()

    k_min = "[" + ks[random.randint(int(len(ks)/5), int(2*len(ks)/5))]
    # k_min = "[" + "Player_0"

    k_max = "[" + ks[random.randint(int(3*len(ks)/5), int(4*len(ks)/5))]
    # k_max = "[" + "Player_9"

    print("Inserted dict ordered by score:{0} as [value:key]\n".format(str(o_by_score)))

    rval = r.zrange(o_key, 0, -1)
    print("Vals from zrange:{0}\n".format(str(rval)))

    print("Will call: zrangebylex({0}, {1}, {2})".format(o_key, k_min, k_max))
    rval = r.zrangebylex(o_key, k_min, k_max)

    print("Type from zrangebylex:{0}\n".format(type(rval)))
    print("Vals from zrangebylex:{0}\n".format(str(rval)))


    ordered_scores = list(set(o_dict.values()))
    ordered_scores.sort()
    score_min = ordered_scores[random.randint(0, int(len(ordered_scores)/3))]
    score_max = ordered_scores[random.randint(int(len(2*ordered_scores)/3), len(ordered_scores)-1)]

    print("Will call: zrangebyscore({0}, {1}, {2})".format(o_key, score_min, score_max))
    rval = r.zrangebyscore(o_key, score_min, score_max)

    print("Inserted dict ordered by name:{0} as [name:score]\n".format(str(o_by_name)))
    print("Type from zrangebyscore:{0}\n".format(type(rval)))
    print("Vals from zrangebyscore:{0}\n".format(str(rval)))

##########################

if __name__ == "__main__":
    # o_set_try_a()
    # zrangeby_try_b()

    o_set_try_a()
