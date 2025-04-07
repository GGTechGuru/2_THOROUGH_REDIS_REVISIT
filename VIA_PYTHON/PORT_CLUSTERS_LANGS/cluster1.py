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

def get_nodes_try_a():

    rc = rcluster_global
    if (rc.ping()):
        print("Cluster is responding")
    else:
        print("Cluster is non-responsive")

    rval = rc.get_nodes()

    rval_type = str(type(rval))
    if 'list' not in rval_type:
        print("Expected get_nodes() to return list, but got type:{0}".format(
            rval_type))

        return

    else:
        # rval = [str(x) for x in rval]
        rval = list( map ( str, rval ) )
        rval.sort()

        print("rc.get_nodes() returned")
        for node in rval:
            print(str(node))

################################

def set_try_b():

    rc = rcluster_global

    rc.delete("tags")

    rc.sadd("tags", "java", "redis", "programming")
    rc.sadd("tags", "one_more_member")

    tags = rc.smembers("tags")

    print(str(tags))

    rc.srem("tags", "java")
    rc.sadd("tags", "python")

    tags = rc.smembers("tags")

    for mem in tags:
        tags.remove(mem)
        tags.add(mem.decode("utf-8"))

    print(str(tags))

    print("Is 'java' a 'tags' set member:{0}".format(rc.sismember("tags", "java")))
    print("Is 'python' a 'tags' set member:{0}".format(rc.sismember("tags", "python")))

##########################

def target_nodes_try_c():

    rc = rcluster_global

    rval = rc.get_nodes()
    ref_node = rval[random.randint(0, len(rval)-1)]
    ref_host = ref_node.host
    ref_port = ref_node.port

    print("ref_host:{0}, ref_port:{1}".format(ref_host, ref_port))

    rval = rc.cluster_meet(ref_host, ref_port, target_nodes=RedisCluster.ALL_NODES)
    print("rval from cluster_meet():{0}".format(str(rval)))

    if (rc.ping(target_nodes=RedisCluster.REPLICAS)):
        print("Cluster replicas are responsive")

    if (rc.ping(target_nodes=RedisCluster.PRIMARIES)):
        print("Cluster primaries are responsive")

    rval = rc.keys(target_nodes=RedisCluster.ALL_NODES)
    print("rc.keys() from ALL_NODES returned:{0}".format(str(rval)))

    rval = rc.keys(target_nodes=RedisCluster.PRIMARIES)
    print("rc.keys() from PRIMARIES returned:{0}".format(str(rval)))

    rval = rc.keys(target_nodes=RedisCluster.REPLICAS)
    print("rc.keys() from REPLICAS returned:{0}".format(str(rval)))

    rval = rc.keys(target_nodes=RedisCluster.RANDOM)
    print("rc.keys() from a RANDOM node returned:{0}".format(str(rval)))

##########################

def save_ops_try_d():

    rc = rcluster_global
    some_key = str(time.time()).split(".")[-1]
    time.sleep(random.random())
    some_val = str(time.time()).split(".")[-1]
    status = rc.set(some_key, some_val)
    rval = rc.bgsave(target_nodes=RedisCluster.PRIMARIES)
    print("Return from bgsave:{0}".format(str(rval)))

    try:
        rval = rc.save(target_nodes=RedisCluster.PRIMARIES)
        print("Return from save:{0}".format(str(rval)))
    except Exception as e:
        print("Call to save() got exception message:{0}".format(str(e.args[0])))

    print(str(rc.keys(target_nodes=RedisCluster.ALL_NODES)))


##########################

def info_try_e():

    rc = rcluster_global
    
    rval = rc.get_primaries()
    print("rval from get_primaries():{0}".format(str(rval)))

    rval = rc.info()
    print("rval from info():{0}".format(str(rval)))

    rval = rc.cluster_info()
    print("rval from cluster_info():{0}".format(str(rval)))

##########################

def cluster_shards_try_g():

    rc = rcluster_global
    
    rval = rc.cluster_shards()
    print("rval from cluster_shards():{0}".format(str(rval)))

    rval = rc.cluster_slots()
    print("rval from cluster_slots():{0}".format(str(rval)))

##########################

def cluster_links_try_i():

    rc = rcluster_global
    
    rval = rc.cluster_links(RedisCluster.PRIMARIES)
    print("rval from cluster_links(PRIMARIES):{0}".format(str(rval)))

    rval = rc.cluster_links(RedisCluster.REPLICAS)
    print("rval from cluster_links(REPLICAS):{0}".format(str(rval)))

    rval = rc.cluster_links(RedisCluster.ALL_NODES)
    print("rval from cluster_links(ALL_NODES):{0}".format(str(rval)))

##########################

def cluster_get_keys_in_slot_try_k():

    rc = rcluster_global
    
    rval = rc.keys()
    print("rval from keys():{0}".format(str(rval)))

    rval = rc.cluster_slots()
    print("rval from cluster_slots():{0}".format(str(rval)))

    min_slot = list(rval.keys())[0][0]
    max_slot = list(rval.keys())[0][1]
    srl = []
    for slot_range in list(rval.keys()):
        srl.append(slot_range)
        if (min_slot > slot_range[0]):
            min_slot = slot_range[0]

        if (max_slot < slot_range[1]):
            max_slot = slot_range[1]

    # print("Slot range type::{0}".format(str(type(srl[0]))))

    slot_with_keys = None
    for slot_num in range(min_slot, max_slot):
        rval = rc.cluster_countkeysinslot(slot_num)
        if rval > 0:
            slot_with_keys = slot_num
            print("Slot {0} has {1} keys".format(slot_num, rval))

            break

    # rand_index = random.randint(0, len(srl)-1)
    # rand_range = srl[rand_index]
    # print("Random range::{0}".format(rand_range))

    # rand_slot = random.randint(rand_range[0], rand_range[1])
    # print("Random slot::{0}".format(rand_slot))

    # rval = rc.cluster_get_keys_in_slot(rand_slot, 100)
    rval = rc.cluster_get_keys_in_slot(slot_with_keys, 100)
    print("Return from cluster_get_keys_in_slot({0})::{1}".format(slot_with_keys, str(rval)))

#################################

def cluster_del_add_slots_try_l():

    rc = rcluster_global
    
    # rval = rc.keys()
    # print("rval from keys():{0}".format(str(rval)))

    rval = rc.cluster_slots()
    print("rval from cluster_slots():{0}".format(str(rval)))

    srl = list(rval.keys())
    rand_index = random.randint(0, len(srl)-1)
    rand_range = srl[rand_index]
    print("Random range::{0}".format(rand_range))

    rand_slot_subrange = None

    slot_sr_init = random.randint(rand_range[0], (rand_range[0] + int((rand_range[1] - rand_range[0])/3)))
    slot_sr_end = random.randint(slot_sr_init+1, (slot_sr_init + 1 + 2*int((rand_range[1] - rand_range[0])/3)))

    slot_sr_end = min(slot_sr_end, rand_range[1])
    slot_sr_init = min(slot_sr_init, slot_sr_end)

    while (slot_sr_init < slot_sr_end) and (rc.cluster_countkeysinslot(slot_sr_init) > 0):
        slot_sr_init += 1

    if rc.cluster_countkeysinslot(slot_sr_init) > 0:
        print("Did not, in first attempt, find empty slot range for deletion test")
        return

    slot_in_between = slot_sr_init + 1
    while (slot_in_between <= slot_sr_end) and (rc.cluster_countkeysinslot(slot_in_between) == 0):
        slot_in_between += 1

    slot_sr_end = slot_in_between - 1

    del_range = (slot_sr_init, slot_sr_end)
    for del_slot in range(del_range[0], del_range[1]+1):
        try:
            rval = rc.cluster_delslots(del_slot)
            print("rval from cluster_delslots({0})::{1}".format(del_slot, str(rval)))
        except Exception as e:
            print("Exception after cluster_delslots({0})::{1}".format(del_slot, str(e.args[0])))
            continue

    rval = rc.cluster_slots()

    slots_remaining = list(rval.keys())
    for slot_range in slots_remaining:
        range_overlap = False
        if (del_range[0] >= slot_range[0]) and (del_range[0] <= slot_range[1]):
            # print("ERROR: Deleted slot range {0} overlaps with existing range {1}".format(str(del_range), str(slot_range)))
            range_overlap = True

        elif (del_range[1] >= slot_range[0]) and (del_range[1] <= slot_range[1]):
            # print("ERROR: Deleted slot range {0} overlaps with existing range {1}".format(str(del_range), str(slot_range)))
            range_overlap = True

        if range_overlap:
            print("ERROR: Deleted slot range {0} overlaps with existing range {1}".format(str(del_range), str(slot_range)))
            # break


    # add_range = del_range.copy()
    add_range = (del_range[0], del_range[1])
    for slot_to_add in range(add_range[0], add_range[1]+1):
        try:
            rval = rc.cluster_addslots(RedisCluster.ALL_NODES, slot_to_add)
            print("Return from addslots({0}) is::{1}".format(slot_to_add, str(rval)))
        except Exception as e:
            print("Exception after cluster_addslots({0})::{1}".format(slot_to_add, str(e.args[0])))
            continue

    slots_now = list(rval.keys())
    readded_slots_set = {e for e in range(add_range[0], add_range[1]+1)}
    missing_slots_set = readded_slots_set.copy()

    for slot_range in slots_now:
        this_range_set = {e for e in range(slot_range[0], slot_range[1]+1)}
        missing_slots_set = missing_slots_set - this_range_set

        if (len(missing_slots_set) < 1):
            break

    missing_slots_list = list(missing_slots_set)
    missing_slots_list.sort()
    if (len(missing_slots_set) >= 1):
        print("ERROR: These slots were not succesfully added back::{0}".format(str(missing_slots_list)))

###################################################################################################################

def cluster_del_add_slots_range_try_m():

    rc = rcluster_global
    
    # rval = rc.keys()
    # print("rval from keys():{0}".format(str(rval)))

    rval = rc.cluster_slots()
    print("rval from cluster_slots():{0}".format(str(rval)))

    srl = list(rval.keys())
    rand_index = random.randint(0, len(srl)-1)
    rand_range = srl[rand_index]
    print("Random range::{0}".format(rand_range))

    rand_slot_subrange = None

    slot_sr_init = random.randint(rand_range[0], (rand_range[0] + int((rand_range[1] - rand_range[0])/3)))
    slot_sr_end = random.randint(slot_sr_init+1, (slot_sr_init + 1 + 2*int((rand_range[1] - rand_range[0])/3)))

    slot_sr_end = min(slot_sr_end, rand_range[1])
    slot_sr_init = min(slot_sr_init, slot_sr_end)

    while (slot_sr_init < slot_sr_end) and (rc.cluster_countkeysinslot(slot_sr_init) > 0):
        slot_sr_init += 1

    if rc.cluster_countkeysinslot(slot_sr_init) > 0:
        print("Did not, in first attempt, find empty slot range for deletion test")
        return

    slot_in_between = slot_sr_init + 1
    while (slot_in_between <= slot_sr_end) and (rc.cluster_countkeysinslot(slot_in_between) == 0):
        slot_in_between += 1

    slot_sr_end = slot_in_between - 1

    del_range = (slot_sr_init, slot_sr_end)
    try:
        rval = rc.cluster_delslotsrange(del_range[0], del_range[1])
        print("rval from cluster_delslotsrange({0})::{1}".format(str(del_range), str(rval)))
    except Exception as e:
        print("Exception after cluster_delslotsrange({0})::{1}".format(str(del_range), str(e.args[0])))

    rval = rc.cluster_slots()

    slots_remaining = list(rval.keys())
    range_overlap = False
    for slot_range in slots_remaining:
        if (del_range[0] >= slot_range[0]) and (del_range[0] <= slot_range[1]):
            range_overlap = True

        elif (del_range[1] >= slot_range[0]) and (del_range[1] <= slot_range[1]):
            range_overlap = True

        if range_overlap:
            print("ERROR: Deleted slot range {0} overlaps with existing range {1}".format(str(del_range), str(slot_range)))
            break


    try:
        rval = rc.cluster_addslotsrange(RedisCluster.ALL_NODES, del_range[0], del_range[1])
        print("Return from addslotrange({0}) is::{1}".format(str(del_range), str(rval)))
    except Exception as e:
        print("Exception after cluster_addslotsrange({0})::{1}".format(str(del_range), str(e.args[0])))

    slots_now = list(rval.keys())
    readded_slots_set = {e for e in range(del_range[0], del_range[1])}
    missing_slots_set = readded_slots_set.copy()

    for slot_range in slots_now:
        this_range_set = {e for e in range(slot_range[0], slot_range[1])}
        missing_slots_set = missing_slots_set - this_range_set

        if (len(missing_slots_set) < 1):
            break

    missing_slots_list = list(missing_slots_set)
    missing_slots_list.sort()
    if (len(missing_slots_set) >= 1):
        print("ERROR: These slots were not succesfully added back::{0}".format(str(missing_slots_list)))

##########################

def cluster_replicas_try_n():

    rc = rcluster_global

    rval = rc.cluster_nodes()

    primaries = []
    for node in rval.values():
        if 'master' in node["flags"]:
            node_id = node["node_id"]
            primaries.append(node_id)

            rval = rc.cluster_replicas(node_id)
            print("cluster_replicas({0}) returned::{1}\n".format(node_id, str(rval)))

##########################

def cluster_failover_try_p():

    rc = rcluster_global

    rval = rc.cluster_nodes()
    print(str(rval))

    replicas = []
    for node in rval.values():
        if not ('master' in node["flags"]):
            node_id = node["node_id"]
            replicas.append(node_id)

    print("Replica node ID's::{0}".format(str(replicas)))

    # node_id = replicas[random.randint(0, len(replicas)-1)]
    # rval = rc.cluster_failover(node_id)
    rval = rc.cluster_failover(RedisCluster.REPLICAS)
    # print("cluster_failover({0}) returned::{1}\n".format(node_id, str(rval)))
    print("cluster_failover({0}) returned::{1}\n".format(str(RedisCluster.REPLICAS), str(rval)))

    rval = rc.cluster_nodes()
    print(str(rval))

##########################

if __name__ == "__main__":

    # get_nodes_try_a()
    # set_try_b()
    # target_nodes_try_c()
    # save_ops_try_d()
    # info_try_e()
    # cluster_shards_try_g()
    # cluster_links_try_i()
    # cluster_get_keys_in_slot_try_k()
    # cluster_del_add_slots_try_l()
    # cluster_del_add_slots_range_try_m()

    # cluster_replicas_try_n()

    cluster_failover_try_p()
