#! /usr/bin/python3

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

def dir_try_a():

    rs = rsentinels_global

    print(dir(rs))

################################

def sentinels_try_b():

    rs = rsentinels_global

    sentinels_list = rs.sentinels

    print("Subset of details retrieved from Sentinel.sentinels::\n")
    for sentinel in sentinels_list:
        rcp = sentinel.connection_pool
        # print("rcp.__dict__::{0}".format(str(rcp.__dict__)))

        conn_details = rcp.__dict__['connection_kwargs']
        # print("conn_details::{0}".format(str(conn_details)))

        host_port = (conn_details['host'], conn_details['port'])
        print("(host, port)=={0}".format(str(host_port)))

################################

if __name__ == "__main__":

    # dir_try_a()

    sentinels_try_b()
