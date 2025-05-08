#! /home/winitall/MC_SHARE/Desktop/THOROUGH_PYTHON/LEARN_ENV/bin/python3

from redis.sentinel import Sentinel

import os
import random
import sys
import time

##############################

def set_sentinels_conn():

    rc = None

    sentinel_addrs = os.getenv("REDIS_SENTINEL_ADDRS")

    if (sentinel_addrs is None):
        print("Set REDIS_SENTINEL_ADDRS env to '<sentinel-ip1>:port1,<sentinel-ip2>:port2,... ' to run this.")
        sys.exit(2)

    sentinel_addrs_list = sentinel_addrs.split(",")

    sentinel_addr_tuples = []
    for addr_pair in sentinel_addrs_list:
        host_addr_as_list = addr_pair.split(":")
        host_str = host_addr_as_list[0]
        port_int = int(host_addr_as_list[1])
        sentinel_tuple = (host_str, port_int)

        sentinel_addr_tuples.append(sentinel_tuple)

    # print(str(sentinel_addr_tuples))

    return Sentinel(sentinel_addr_tuples)

################################

rsentinels_global = set_sentinels_conn()

################################

def master_for_try_a():

    rs = rsentinels_global

    srvs = os.getenv("REDIS_SERVICE_NAMES")

    if srvs is None:
        print("TO run this test: set REDIS_SERVICE_NAMES as '<service-name-1>,<service-name-2>,...'")
        return False

    srvl = srvs.split(",")

    for srv in srvl:
        md = rs.discover_master(srv)
        print("Return from discover_master({0})::{1}".format(srv, md))

        sd = rs.discover_slaves(srv)
        print("Return from discover_slaves({0})::{1}".format(srv, sd))

    for srv in srvl:
        mf = rs.master_for(srv)
        sf = rs.slave_for(srv)

        some_key = str(random.random()).split(".")[-1]
        some_val = str(random.random()).split(".")[-1]

        mf.set(some_key, some_val)
        rval = sf.get(some_key)

        print("In master({0}), set::({1}, {2}). From slave, got value::{3}".format(srv, some_key, some_val, rval))

################################

if __name__ == "__main__":

    master_for_try_a()

