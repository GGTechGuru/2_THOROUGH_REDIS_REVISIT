#! /usr/bin/python3

import redis
import os

import random
import time


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
def geo_try_a():

    r = rconn_global

    r.delete("India")

    loc_list = [
        (78, 12, "Dharmapuri"),
        (80.17, 13.04, "Chennai"),
        (77.56, 12.97, "Bengaluru"),
        (76.971, 11.0161, "Coimbatore"),
        (76, 10, "Kochi"),
        (74.88, 12.87, "Mangalore"),
        (77.1, 13.34, "Tumkur"),
        (77.543, 13.292, "Dodballapura"),
    ]

    # coords = (12, 78, "Dharmapuri")

    for coords in loc_list:
        r.geoadd("India", coords)


    rval = r.geohash("India", "Bengaluru", "Tumkur")
    print("\ngeohash():{0}".format(str(rval)))

    rval = r.geopos("India", "Bengaluru", "Tumkur")
    print("\ngeopos(India, Bengaluru, Tumkur):{0}".format(str(rval)))

    # rval = r.geosearch("India", "FROMLONLAT", 77, 13,  "BYRADIUS", 200, "km", "ASC")
    rval = r.geosearch("India", longitude=77, latitude=13, unit="km", radius=200, sort="ASC")
    print("\ngeosearch(India, 77, 13, radius=200 km):{0}".format(str(rval)))

    rval = r.geosearch("India", longitude=76, latitude=10, unit="km", width=1300, height=700, sort="ASC")
    print("\ngeosearch(India, 75, 9, width=1300 km, height=700 km):{0}".format(str(rval)))

    rval = r.geosearchstore("loc_rect1", "India", longitude=76, latitude=10, unit="km", width=1300, height=700, sort="ASC")
    print("\ngeosearchstore(loc_rect1...):{0}".format(str(rval)))

    rval = r.geosearch("loc_rect1", member="Kochi", radius=2000, unit="km")
    print("\ngeosearch(loc_rect1):{0}".format(str(rval)))

    # rval = r.debug_object("loc_rect1")
    # rval = r.debug_object("India")
    # print("\ndebug_object(loc_rect1):{0}".format(str(rval)))

    for startx in range(0, len(loc_list)-1):
        p0 = loc_list[startx][2]
        for destx in range(startx+1, len(loc_list)):
            p1 = loc_list[destx][2]

            dist = r.geodist("India", p0, p1)

            print("dist from {0} to {1} is {2}".format(p0, p1, dist))

    for startx in range(0, len(loc_list)):
        longitude = loc_list[startx][0]
        latitude = loc_list[startx][1]
        p0 = loc_list[startx][2]

        distance = 200
        dist_unit = "km"
        inrange = r.georadius("India", longitude, latitude, distance, dist_unit)

        # print(str(inrange))
        inrange = [p.decode("utf-8") for p in inrange]
        inrange.remove(p0)

        inrange.sort()

        if len(inrange) > 1:
            prose_range = ", ".join(inrange[0:len(inrange)-1])
            prose_range += " and {0}".format(inrange[-1])

        elif len(inrange) == 1:
            prose_range = inrange[0]

        else:
            prose_range = "none"

        print("Places within {0} {1} of {2} are {3}.".format( distance, dist_unit, p0, str(prose_range)))



###########################

if __name__ == "__main__":
    geo_try_a()

