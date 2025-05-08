#! /usr/bin/python3

from redis.cluster import RedisCluster
from redis.cluster import ClusterNode

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

def srandmember_try_a():

    rc = rcluster_global

    rc.delete("tags")

    rc.sadd("tags", "java", "redis", "programming")
    rc.sadd("tags", "one_more_member")

    print("scard():{0}".format(rc.scard("tags")))
    print(str(rc.smembers("tags")))

    for i in range(0, 3):
        rval = rc.srandmember("tags")
        print("rc.srandmember() returns:{0}".format(str(rval)))

    for i in range(0, 3):
        count = random.randint(1, rc.scard("tags") * 2)
        rval = rc.srandmember("tags", count)
        print("rc.srandmember({0}) returns:{1}".format(count, str(rval)))

##########################

def spop_try_b():

    rc = rcluster_global

    rc.delete("tag1")
    for count in range(0,20):
        some_val = str(time.time()).split(".")[-1]
        rc.sadd("tag1", some_val)

    rval = rc.smembers("tag1")
    py_set_main = set(rval)
    print("smembers('tag1'):{0}".format(str(rval)))

    for index in range( 0, int(rc.scard("tag1")/5) ):
        rval = rc.spop("tag1")
        py_set_main -= {rval}
        print("rval from spop():{0}".format(str(rval)))

        set_main = rc.smembers("tag1")
        # print("Remaining smembers('tag1'):{0}".format(str(rc.smembers("tag1"))))

        diff_set = py_set_main ^ set_main
        if len(diff_set) > 0:
            print("Diff from py set ops: {0}".format(str(diff_set)))


    rc.delete("tag1")
    for index in range(0,100):
        some_val = str(time.time()).split(".")[-1]
        rc.sadd("tag1", some_val)

    # print("smembers('tag1'):{0}".format(str(rc.smembers("tag1"))))
    rval = rc.smembers("tag1")
    py_set_main = set(rval)
    print("smembers('tag1'):{0}".format(str(rval)))

    for index in range( 0, int(rc.scard("tag1")/5) ):
        count = random.randint( 2, int(rc.scard("tag1") / 10) + 2 )
        rval = rc.spop("tag1", count)

        py_set_main -= set(rval)

        # print("rval from spop('tag1', {0}):{1}".format(count, str(rval)))

        # print("Remaining smembers('tag1'):{0}".format(str(rc.smembers("tag1"))))
        set_main = rc.smembers("tag1")

        diff_set = py_set_main ^ set_main
        if len(diff_set) > 0:
            print("Diff from py set ops: {0}".format(str(diff_set)))

        
##########################

if __name__ == "__main__":

    # srandmember_try_a()

    spop_try_b()
