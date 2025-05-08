#! /home/winitall/MC_SHARE/Desktop/THOROUGH_PYTHON/LEARN_ENV/bin/python3

import os
import random
import subprocess
import time

##############################

# SENTINEL replicas myprimary
# redis-cli -u redis://localhost:50005

def exec_cli(cli, cmd_to_cli):
    
    cmd, temp = os.pipe()
    
    os.write(temp, bytes("{0}\n".format(cmd_to_cli), "utf-8"))
    os.close(temp)

    s = subprocess.check_output( cli, stdin=cmd, shell=True )

    return(s.decode("utf-8"))

##############################

def serial_to_dicts(as_lines):
    rd_l = []

    as_list = as_lines.split("\n")
    l = len(as_list)-1
    while len(as_list[l]) < 1:
        l -= 1
    as_list = as_list[0:l+1]

    # print("Mod len(as_list)::{0}".format(len(as_list)))

    rd = {}
    index = 0;
    while index <= len(as_list)-2:
        if (as_list[index] in rd.keys()):
            rd_l.append(rd)
            rd = {}

        rd[as_list[index]] = as_list[index+1]
        index += 2

        # print("index::{0}".format(index))

    rd_l.append(rd)

    return rd_l

##############################

def rand_sentinel():

    sentinel_addrs = os.getenv("REDIS_SENTINEL_ADDRS")
    if sentinel_addrs is None:
        print("To call this function: set REDIS_SENTINEL_ADDRS as '<host1>:<port1>,<host2>:<port2>,...'")
        return None

    addr_list = sentinel_addrs.split(",")
    rand_index = random.randint(0, len(addr_list)-1)
    rand_sentinel = addr_list[rand_index]

    return rand_sentinel

##############################
def servs_list():

    srvs = os.getenv("REDIS_SERVICE_NAMES")
    if srvs is None:
        print("To call this function: set REDIS_SERVICE_NAMES as '<service-name-1>,<service-name-2>,...'")
        return None

    srvl = srvs.split(",")
    return srvl

##############################

def sentinel_replicas_try_a():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    for srv in servs_list():
        cmd_to_cli = "SENTINEL replicas {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)
        
        print("\nReturn from '{0} {1}'::\n".format(cli, cmd_to_cli))
        for en in serial_to_dicts(rval):
            print(en)


##############################

def sentinel_sentinels_try_b():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    for srv in servs_list():
        cmd_to_cli = "SENTINEL sentinels {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)
        
        print("\nReturn from '{0} {1}'::\n".format(cli, cmd_to_cli))
        for en in serial_to_dicts(rval):
            print(en)

##############################

def sentinel_master_try_c():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    for srv in servs_list():
        cmd_to_cli = "SENTINEL master {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)

        print("\nReturn from '{0} {1}'::\n".format(cli, cmd_to_cli))
        for en in serial_to_dicts(rval):
            print(en)


##############################

def sentinel_masters_try_e():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "SENTINEL MASTERS"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n".format(cli, cmd_to_cli))
    for en in serial_to_dicts(rval):
        print(en)

##############################

def sentinel_config_get_try_g():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "SENTINEL CONFIG GET *"
    rval = exec_cli(cli, cmd_to_cli)

    # print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))
    print("\nReturn from '{0} {1}'::\n".format(cli, cmd_to_cli))
    for en in serial_to_dicts(rval):
        print(en)

##############################

def sentinel_ckquorum_try_i():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    for srv in servs_list():
        cmd_to_cli = "SENTINEL CKQUORUM {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)

        print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))


##############################

def sentinel_get_master_addr_by_name_try_k():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    for srv in servs_list():
        cmd_to_cli = "SENTINEL GET-MASTER-ADDR-BY-NAME {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)

        print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_info_try_l():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "INFO"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_myid_try_n():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "SENTINEL MYID"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_ping_try_p():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "PING"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_role_try_q():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "ROLE"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_pending_scripts_try_r():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "SENTINEL PENDING-SCRIPTS"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_simulate_failure_try_s():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "SENTINEL SIMULATE-FAILURE HELP"
    rval = exec_cli(cli, cmd_to_cli)
    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

    cmd_to_cli = "SENTINEL SIMULATE-FAILURE CRASH-AFTER-ELECTION"
    rval = exec_cli(cli, cmd_to_cli)
    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

    cmd_to_cli = "SENTINEL SIMULATE-FAILURE CRASH-AFTER-PROMOTION"
    rval = exec_cli(cli, cmd_to_cli)
    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

    print("CAUTION: SENTINEL FAILURE WILL OCCUR WHEN THESE TRIGGERS HAPPEN SUBSEQUENTLY!!")

###########################################################################################

def sentinel_failover_try_t():

    failover_seconds = 60

    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    for srv in servs_list():
        cmd_to_cli = "SENTINEL MASTER {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)
        print("\nReturn before failover initiation from '{0} {1}'::\n".format(cli, cmd_to_cli))
        for en in serial_to_dicts(rval):
            print(en)

    for srv in servs_list():
        cmd_to_cli = "SENTINEL FAILOVER {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)
        print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

    print("ATTENTION: Will now wait {0} seconds while failover occurs.".format(failover_seconds))
    time.sleep(failover_seconds)

    for srv in servs_list():
        cmd_to_cli = "SENTINEL MASTER {0}".format(srv)
        rval = exec_cli(cli, cmd_to_cli)

        print("\nReturn {0} seconds after failover initiation from '{1} {2}'::\n".format(failover_seconds, cli, cmd_to_cli))
        for en in serial_to_dicts(rval):
            print(en)


##############################

def sentinel_flushconfig_try_u():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "SENTINEL FLUSHCONFIG"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

##############################

def sentinel_command_list_try_v():
    cli = "redis-cli -u redis://{0}".format(rand_sentinel())

    cmd_to_cli = "COMMAND LIST"
    rval = exec_cli(cli, cmd_to_cli)

    print("\nReturn from '{0} {1}'::\n{2}".format(cli, cmd_to_cli, rval))

#################################################################################

if __name__ == "__main__":
    # sentinel_replicas_try_a()
    # sentinel_sentinels_try_b()
    # sentinel_master_try_c()
    # sentinel_masters_try_e()
    # sentinel_masters_try_e()
    # sentinel_config_get_try_g()
    # sentinel_ckquorum_try_i()
    # sentinel_get_master_addr_by_name_try_k()
    # sentinel_info_try_l()
    # sentinel_myid_try_n()
    # sentinel_info_try_l()
    # sentinel_ping_try_p()
    # sentinel_role_try_q()
    # sentinel_pending_scripts_try_r()
    # sentinel_simulate_failure_try_s()
    # sentinel_failover_try_t()
    # sentinel_flushconfig_try_u()

    sentinel_command_list_try_v()
