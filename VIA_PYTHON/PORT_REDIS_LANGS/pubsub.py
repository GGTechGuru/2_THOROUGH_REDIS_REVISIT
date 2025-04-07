#! /usr/bin/python3

import redis

import multiprocessing

import numpy

import random

import time

####################################

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

####################################

def sel_pub_info(chan):
   return "Some content: " + str(chan)

####################################

def publisher(chan_list, max_sec):

    end_times = time.time() + max_sec

    r = rconn_global

    chan_count = len(chan_list)

    while (time.time() < end_times):

        print("Publisher: Time.time():{0}".format(str(time.time())))

        time.sleep(random.random() * 4)

        chan_index = int(random.random() * chan_count)
        now_chan = chan_list[chan_index]

        now_info = sel_pub_info(now_chan)

        r.publish(now_chan, now_info)

########################

def subscriber(chan_list, max_sec):

    end_times = time.time() + max_sec

    r = rconn_global

    s = r.pubsub()

    for chan in chan_list:
        s.subscribe(chan)

    while (time.time() < end_times):

        # print("Subscriber: Time.time():{0}".format(str(time.time())))

        time.sleep(random.random() * 1)

        msg = s.get_message()
        while msg is not None:
            print("Msg:{0}".format(str(msg)))
            msg = s.get_message()

########################

if __name__ == "__main__":

    all_pub_chans = dir(numpy)
    all_sub_chans = all_pub_chans

    pub_max_sec = 60
    sub_max_sec = 60

    processes = []


    for index in range(0,10):
        shuffled_apc = all_pub_chans[:]
        random.shuffle(shuffled_apc)
        pub_chans = shuffled_apc[:5]

        print("pub_chans:{0}".format(str(pub_chans)))

        pp = multiprocessing.Process(target=publisher, args=(pub_chans, pub_max_sec))
        processes.append(pp)


    for index in range(0,4):
        shuffled_asc = all_sub_chans[:]
        random.shuffle(shuffled_asc)

        sub_chans = shuffled_asc[:int(len(all_sub_chans)/2.0)]

        # sub_chans = all_sub_chans

        print("sub_chans:{0}".format(str(sub_chans)))

        sp = multiprocessing.Process(target=subscriber, args=(sub_chans, sub_max_sec))
        processes.append(sp)

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()
