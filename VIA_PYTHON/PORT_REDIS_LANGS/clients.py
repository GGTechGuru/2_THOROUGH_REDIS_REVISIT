#! /usr/bin/python3

import redis

import os
import time

import multiprocessing

import psutil

def set_conn():
    tp_str = os.getenv("REDIS_TEST_PORT")
    if tp_str is not None:
        test_port=int(tp_str)
        r = redis.Redis(port=test_port)
    else:
        r = redis.Redis()

    return r

################################

rconn_global = set_conn()

################################

def find_conns(fltr_pids, r_ip, r_port):
    ncs = psutil.net_connections()

    nc_by_pid = {}
    for nc in ncs:

        # print("Next nc:{0}".format(str(nc)))

        if nc.pid not in nc_by_pid.keys():
            nc_by_pid[nc.pid] = []
            
        nc_by_pid[nc.pid].append(nc)

    fltr_conns = []

    for fltr_pid in fltr_pids:

        print("Is fltr_pid:{0} in nc_by_pid.keys():{1}".format(fltr_pid, str(nc_by_pid.keys())))
        print(fltr_pid in nc_by_pid.keys())

        if fltr_pid not in nc_by_pid.keys():
            continue
        else:
            for nc in nc_by_pid[fltr_pid]:

                print("nc.raddr.ip:[{0}] ?= r_ip:[{1}] nc.raddr.port:[{2}] ?= r_port:[{3}]".format(
                    nc.raddr.ip, r_ip, nc.raddr.port, r_port))

                print("Type of each nc.raddr.ip:[{0}] ?= r_ip:[{1}] nc.raddr.port:[{2}] ?= r_port:[{3}]".format(
                    type(nc.raddr.ip), type(r_ip), type(nc.raddr.port), type(r_port)))

                print("Is nc.raddr.ip == r_ip and nc.raddr.port == r_port")
                print(nc.raddr.ip == r_ip and nc.raddr.port == r_port)

                if (nc.raddr.ip == r_ip and nc.raddr.port == r_port):
                    l_ip = nc.laddr.ip
                    l_port = nc.laddr.port

                    l_conn = {
                        "l_ip" : l_ip,
                        "l_port" : l_port,
                        "l_conn_str" : "{0}:{1}".format(l_ip, l_port)
                    }

                    fltr_conns.append(l_conn)

                    print("Current fltr_conns len:{0}".format(len(fltr_conns)))

    return fltr_conns

################################

def client_connect(hold_sec=60):
    r = rconn_global
    some_key = str(time.time())
    status = r.set(some_key, "aval")

    # print("Client pid:{0}".format(str(os.getpid())))
    time.sleep(hold_sec)

################################

def client_list_try_a():

    r = rconn_global

    proclist = []

    for i in range(0,10):
        proc = multiprocessing.Process(target=client_connect, args=(30,))
        proclist.append(proc)

    for proc in proclist:
        proc.start()


    exp_pids = [os.getpid()]
    for proc in proclist:
        pid = proc.pid
        exp_pids.append(pid)
        # if pid in ncl_by_pid:
            # matching_ncls.append(ncl_by_pid[pid])
        # else:
            # print("Did not find expected pid:{0} in net_connections list".format(pid))
    print("Expected pids:{0}".format(str(exp_pids)))

    redis_ip = "127.0.0.1"
    redis_port = 6379

    found_redis_conns = find_conns(exp_pids, redis_ip, redis_port)
    print("found_redis_conns:{0}".format(str(found_redis_conns)))

    # found_redis_conns_set = set(found_redis_conns)
    # addrs_per_system = map(x["l_conn_str"], x)

    addrs_per_system = [d["l_conn_str"] for d in found_redis_conns]

    addrs_per_system_set = set(addrs_per_system)

    rval = r.client_list()
    addrs_per_cl = []
    for client in rval:
        addr = client["addr"]
        addrs_per_cl.append(addr)

    addrs_per_cl_set = set(addrs_per_cl)

    print("addrs_per_cl_set:{0}".format(str(addrs_per_cl_set)))
    print("addrs_per_system_set:{0}".format(str(addrs_per_system_set)))

    addrs_only_per_cl = addrs_per_cl_set - addrs_per_system_set
    addrs_only_per_system = addrs_per_system_set - addrs_per_cl_set


    print("Addrs from client_list()")
    for addr in addrs_per_cl:
        print(str(addr))

    print("addrs_only_per_cl:{0}".format(str(addrs_only_per_cl)))
    print("addrs_only_per_system:{0}".format(str(addrs_only_per_system)))

    for proc in proclist:
        proc.join()

############################

if __name__ == "__main__":

    client_list_try_a()


