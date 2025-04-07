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

def client_params_try_a():

    rc = rcluster_global

    name_suffix = str(time.time()).split(".")[-1]
    client_new_name = "client_name_{0}".format(name_suffix)

    rval = rc.client_setname(client_new_name)

    set_client_name = rc.client_getname()

    if (set_client_name != client_new_name):
        print("Client name from client_getname()::{0} != requested in setname::{1}".format(set_client_name, client_new_name))

    client_list = rc.client_list()
    print("Return from client_list()::{0}".format(str(client_list)))

    client_id = rc.client_id()
    print("Return from client_id()::{0}".format(str(client_id)))

    client_info = rc.client_info()
    print("Return from client_info()::{0}".format(str(client_info)))

    set_client_name = client_info['name']
    if (set_client_name != client_new_name):
        print("Client name from client_info()::{0} != requested in setname::{1}".format(set_client_name, client_new_name))

################################

def acl_help_try_b():

    rc = rcluster_global
    rval = rc.acl_help()

    print("Return from acl_help()::{0}".format(str(rval)))

################################

def lastsave_try_c():

    rc = rcluster_global
    rval = rc.lastsave()

    print("Return from lastsave()::{0}".format(str(rval)))
##########################
if __name__ == "__main__":

    # client_params_try_a()
    # acl_help_try_b()

    lastsave_try_c()
