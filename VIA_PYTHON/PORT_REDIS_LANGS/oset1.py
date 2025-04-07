#! /usr/bin/python3

import redis

def o_set_try_a():

    o_dict = {
        "PlayerOne":3000.0,
        "PlayerTwo":1500.0,
        "PlayerThree":8200.0
    }

    r = redis.Redis()

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

##########################
if __name__ == "__main__":
    o_set_try_a()
