#! /usr/bin/python3

import redis

import os
import random
import time

# rconn_global = redis.Redis()

def set_conn():

    addr = os.getenv("REDIS_SINGLE_ADDR")

    if addr is not None:
        addr_as_list = addr.split(":")
        ip = addr_as_list[0]
        port = int(addr_as_list[1])
        r = redis.Redis(host=ip, port=port)

    else:
        print("REDIS_SINGLE_ADDR env not set. Using redis default")
        r = redis.Redis()

    return r

################################

rconn_global = set_conn()

################################

def command_count_try_a():

    r = rconn_global

    rval = r.command_count()
    print("command_count() returned::{0}".format(str(rval)))

    rval = r.command_list() # Not implemented via Python library
    cmd_l = list(rval)
    cmd_l = [e.decode("utf-8") for e in cmd_l]
    cmd_l.sort()

    print("command_list() returned::{0}".format(str(cmd_l)))

    # rval = r.command_info() # Not implemented via Python library
    # print("command_info() returned::{0}".format(str(rval)))

    # rval = r.command_flags() # Not implemented via Python library
    # print("command_flags() returned::{0}".format(str(rval)))

    # rval = r.command_docs() # Not implemented via Python library
    # print("command_docs() returned::{0}".format(str(rval)))

################################

def client_params_try_b():

    r = rconn_global

    name_suffix = str(time.time()).split(".")[-1]
    client_new_name = "client_name_{0}".format(name_suffix)

    rval = r.client_setname(client_new_name)

    client_list = r.client_list()
    print("Return from client_list()::{0}".format(str(client_list)))

    client_id = r.client_id()
    print("Return from client_id()::{0}".format(str(client_id)))

    client_info = r.client_info()
    print("Return from client_info()::{0}".format(str(client_info)))

    set_client_name = client_info['name']
    if (set_client_name != client_new_name):
        print("Returned client name::{0} != requested in setname::{1}".format(set_client_name, client_new_name))

##########################
if __name__ == "__main__":
    # command_count_try_a()

    client_params_try_b()
