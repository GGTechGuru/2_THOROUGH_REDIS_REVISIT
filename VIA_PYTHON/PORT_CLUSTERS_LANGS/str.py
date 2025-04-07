#! /usr/bin/python3

from redis.cluster import RedisCluster
# from redis.cluster import ClusterNode

import os
import random
import sys
import time

##############################

def set_cluster_conn():

    rc = None

    cluster_addr = os.getenv("REDIS_CLUSTER_ADDR")
    cluster_url = os.getenv("REDIS_CLUSTER_URL")
    cluster_addrs_csv = os.getenv("REDIS_CLUSTER_ADDRS_CSV")

    if (cluster_addr is None) and \
        (cluster_url is None) and \
        (cluster_addrs_csv is None):

        print("Set REDIS_CLUSTER_ADDR env to '<cluster-ip>:host' to run this.")
        print("or REDIS_CLUSTER_URL to 'redis://<host-url>:<cluster-port>/0'")
        print("or REDIS_CLUSTER_ADDRS_CSV to multiple comma-separated addrs")
        sys.exit(2)

    elif cluster_addr is not None:
        cluster_addr_as_list = cluster_addr.split(":")
        ip = cluster_addr_as_list[0]
        port = int(cluster_addr_as_list[1])
        rc = RedisCluster(host=ip, port=port)

    elif cluster_url is not None:
        rc = RedisCluster.from_url(cluster_url)

    else:
        addrs = cluster_addrs_csv.split(',')
        cluster_nodes = []
        for cluster_addr in addrs:
            cluster_addr_as_list = cluster_addr.split(":")
            ip = cluster_addr_as_list[0]
            port = int(cluster_addr_as_list[1])

            cluster_nodes.append( ClusterNode( ip, port ) )

        rc = RedisCluster( startup_nodes=cluster_nodes )

    return rc

################################

rcluster_global = set_cluster_conn()

################################

def nonatomic_try_a():

    rc = rcluster_global

    kv = {}

    for count in range(0,10):
        some_key = str(time.time()).split(".")[-1]
        time.sleep(random.random())
        some_val = str(time.time()).split(".")[-1]

        kv[some_key] = some_val

    print("Set::{0}".format(str(kv)))
    rc.mset_nonatomic(kv)
    set_vals = list(kv.values())
    set_vals.sort()

    get_vals = rc.mget_nonatomic(kv)
    get_vals = [x.decode("utf-8") for x in get_vals]
    get_vals.sort()
    print("Set values::{0}".format(str(set_vals)))
    print("Get values::{0}".format(str(get_vals)))

    if (len(set_vals) != len(get_vals)):
        print("Number of set values:{0} != get_values:{1}".format(len(set_vals), len(get_vals)))

    for index in range(0, len(set_vals)):
        if get_vals[index] != set_vals[index]:
            print("Different values in list[{0}]".format(index))

##########################

if __name__ == "__main__":

    nonatomic_try_a()
