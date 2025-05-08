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

def keyslot_try_a():

    rc = rcluster_global

    kv = {}

    key_list = []

    for count in range(0,10):
        some_key = str(time.time()).split(".")[-1]
        time.sleep(random.random())
        some_val = str(time.time()).split(".")[-1]

        kv[some_key] = some_val

        rval = rc.set(some_key, some_val)

    key_list = list(kv.keys())
    key_count = len(key_list)

    curr_key = key_list[random.randint(0, key_count-1)]

    rval = rc.keyslot(curr_key)

    print("Return from keyslot({0})::{1}".format(curr_key, str(rval)))

##########################

if __name__ == "__main__":

    keyslot_try_a()
