#! /usr/bin/python3

from redis.cluster import RedisCluster
from redis.cluster import ClusterNode

import math
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

def list_pop_try_c():

    rc = rcluster_global

    for mult_flag in range(0, 2):
    
        rc.delete("tag1")
        for count in range(0, int(20 * math.pow(5,mult_flag))):
            some_val = str(time.time()).split(".")[-1]
            rc.lpush("tag1", some_val)
    
        rval = rc.lrange("tag1", 0, -1)
        py_list_main = rval.copy()
        print("lrange('tag1'):{0}".format(str(rval)))
    
        for index in range( 0, int(len(rval)/5) ):

            if len(py_list_main) < 1:
                break
    
            pop_count = None
            if mult_flag == 0:
               pop_count = 1
            else:
                pop_count = random.randint(1, 2*len(py_list_main))

            l_r = random.randint(0, 1)
    
            if l_r == 0:
                if mult_flag == 0:
                    rval = rc.lpop("tag1")
                else:
                    rval = rc.lpop("tag1", pop_count)

                if pop_count >= len(py_list_main):
                    py_list_main = []
                else:
                    py_list_main = py_list_main[pop_count:len(py_list_main)]

                print("rval from lpop():{0}".format(str(rval)))
            else:
                if mult_flag == 0:
                    rval = rc.rpop("tag1")
                else:
                    rval = rc.rpop("tag1", pop_count)

                if pop_count >= len(py_list_main):
                    py_list_main = []
                else:
                    py_list_main = py_list_main[:len(py_list_main)-pop_count]

                print("rval from rpop():{0}".format(str(rval)))
    
            list_main = rc.lrange("tag1", 0, -1)
            print("Remaining lrange('tag1'):{0}".format(str(list_main)))
    
            if (len(list_main) != len(py_list_main)):
                print("Different list lengths from RedisCluster & Python")
    
                print("list_main::{0}".format(str(list_main)))
                print("py_list_main::{0}".format(str(py_list_main)))
    
                return
    
            for index in range(0, len(list_main)):
                if (list_main[index] != py_list_main[index]):
                    print("RedisCluster & Python lists differ at index:{0}".format(index))
                    return
    
            
##########################

def ltrim_try_e():

    rc = rcluster_global

    lkey = str(time.time()).split(".")[-1]
    for index in range(0, 20):
        lval = str(time.time()).split(".")[-1]
        rval = rc.rpush(lkey, lval)

    print("Current list:{0}".format(str(rc.lrange(lkey, 0, -1))))
    for index in range(0, int(rc.llen(lkey)/5)):
        lindex = random.randint(0, int(rc.llen(lkey)/ 3))
        rindex = random.randint(2*lindex+1, int(rc.llen(lkey)))

        rval = rc.ltrim(lkey, lindex, rindex)

        rval = rc.lrange(lkey, 0, -1)

        print("List after ltrim(<key>, {0}, {1})::{2}".format(lindex, rindex, str(rval)))

##########################


if __name__ == "__main__":

    # srandmember_try_a()

    # list_pop_try_c()

    ltrim_try_e()
