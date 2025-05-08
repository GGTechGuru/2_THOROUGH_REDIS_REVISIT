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
def rand_printable(p_len=10):

    rstr = ""

    for i in range(0, p_len):
        rchar = chr(random.randint(ord('a'), ord('z')))
        rstr += rchar

    return rstr


################################

def unsigned_byte_not(tbyte):
    rbyte = 0

    print("Using tbyte::{0}".format(tbyte))

    index = 0
    while index < 8:
        bit_val = (1 << index)
        # print("bit_val::{0}".format(bit_val))

        if (tbyte & bit_val) == 0:
            rbyte = rbyte | bit_val
        # print("rbyte now::{0}".format(rbyte))

        index += 1

    return rbyte

################################

def bitop_and_try_a():

    r = rconn_global

    k1 = rand_printable()
    k2 = rand_printable()
    v1 = rand_printable(random.randint(5,15))
    v2 = rand_printable(random.randint(5,15))
    r.set(k1, v1)
    r.set(k2, v2)

    kdest_and = "kdest_and_" + rand_printable()
    rval = r.bitop("and", kdest_and, k1, k2)
    print("Return from bitop(and) for values({0}, {1}) == {2}".format(v1, v2, rval))
    print("Key-dest::{0}, k1::{1}, k2::{2}".format(kdest_and, k1, k2))

    py_ord_and = ""
    min_len = min(len(v1), len(v2))
    max_len = max(len(v1), len(v2))

    index = 0
    while (index<min_len):
        byte_ord_and = ord(v1[index]) & ord(v2[index])
        chr_and = chr(byte_ord_and)
        py_ord_and += str(chr_and)
        index += 1

    rval=r.get(kdest_and)
    print("Return from dest key ({0})::[{1}]".format(kdest_and, rval.decode("utf-8")))

    print("Expected 'bit ord and' from Python::[{0}]".format(py_ord_and))

##############################################################################################

def bitop_or_try_b():

    r = rconn_global

    k1 = rand_printable()
    k2 = rand_printable()
    v1 = rand_printable(random.randint(5,15))
    v2 = rand_printable(random.randint(5,15))
    r.set(k1, v1)
    r.set(k2, v2)

    kdest_or = "kdest_or_" + rand_printable()
    rval = r.bitop("or", kdest_or, k1, k2)
    print("Return from bitop(or) for values({0}, {1}) == {2}".format(v1, v2, rval))
    print("Key-dest::{0}, k1::{1}, k2::{2}".format(kdest_or, k1, k2))

    py_ord_or = ""
    min_len = min(len(v1), len(v2))
    max_len = max(len(v1), len(v2))

    index = 0
    while (index<min_len):
        byte_ord_or = ord(v1[index]) | ord(v2[index])
        chr_or = chr(byte_ord_or)
        py_ord_or += str(chr_or)
        index += 1

    if (len(v1) > len(v2)):
        py_ord_or += v1[len(v2):len(v1)]
    else:
        py_ord_or += v2[len(v1):len(v2)]

    rval=r.get(kdest_or)
    print("Return from dest key ({0})::[{1}]".format(kdest_or, rval.decode("utf-8")))

    print("Expected 'bit ord or' from Python::[{0}]".format(py_ord_or))

##############################################################################################

def bitop_xor_try_c():

    r = rconn_global

    k1 = rand_printable()
    k2 = rand_printable()
    v1 = rand_printable(random.randint(5,15))
    v2 = rand_printable(random.randint(5,15))
    r.set(k1, v1)
    r.set(k2, v2)

    kdest_xor = "kdest_xor_" + rand_printable()
    rval = r.bitop("xor", kdest_xor, k1, k2)
    print("Return from bitop(xor) for values({0}, {1}) == {2}".format(v1, v2, rval))
    print("Key-dest::{0}, k1::{1}, k2::{2}".format(kdest_xor, k1, k2))

    py_ord_xor = ""
    min_len = min(len(v1), len(v2))
    max_len = max(len(v1), len(v2))

    index = 0
    while (index<min_len):
        byte_ord_xor = ord(v1[index]) ^ ord(v2[index])
        chr_xor = chr(byte_ord_xor)
        py_ord_xor += str(chr_xor)
        index += 1

    if (len(v1) > len(v2)):
        py_ord_xor += v1[len(v2):len(v1)]
    else:
        py_ord_xor += v2[len(v1):len(v2)]

    rval=r.get(kdest_xor)
    print("Return from dest key ({0})::\n[{1}]".format(kdest_xor, rval.decode("utf-8")))

    print("Expected 'bit ord xor' from Python::\n[{0}]".format(py_ord_xor))

##############################################################################################

def bitop_not_try_d():

    r = rconn_global

    k1 = rand_printable()
    v1 = rand_printable(random.randint(5,15))
    r.set(k1, v1)

    kdest_not = "kdest_not_" + rand_printable()
    rval = r.bitop("not", kdest_not, k1)
    print("Return from bitop(not) for value({0}) == {1}".format(v1, rval))
    print("Key-dest::{0}, k1::{1}".format(kdest_not, k1))

    py_ord_not = ""

    index = 0
    while (index<len(v1)):
        # complement = hex(unsigned_byte_not(int(str(v1)[index])))
        byte_val = v1[index]
        complement = unsigned_byte_not(ord(byte_val))

        hex_str = str(hex(complement))
        hex_str = '\\' + hex_str[1::]
        py_ord_not += hex_str

        index += 1

    rval=r.get(kdest_not)
    print("Return from dest key ({0})::\n[{1}]".format(kdest_not, str(rval)))

    print("Expected 'bit ord ^r' from Python::\n[{0}]".format(py_ord_not))

##############################################################################################

def bitcount_try_e():

    r = rconn_global

    k1 = rand_printable()
    v1 = rand_printable(random.randint(5,15))
    r.set(k1, v1)

    bitc_py = 0
    for c in v1:
        bitc_py += ord(c).bit_count()

    bitc_r = r.bitcount(k1)

    # if bitc_r != bitc_py:
    print("Bitcount from Redis.bitcount({0}(key))::{1}. From Py.int.bit_count::{2}".format(k1, bitc_r, bitc_py))

###################################################################################################

if __name__ == "__main__":

    # bitop_and_try_a()
    # bitop_or_try_b()
    # bitop_xor_try_c()
    # bitop_not_try_d()

    bitcount_try_e()

