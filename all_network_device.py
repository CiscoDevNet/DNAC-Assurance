#!/usr/bin/env python

from __future__ import print_function
import json
import logging
import time
import calendar
from datetime import datetime
from argparse import ArgumentParser
from util import post

# often addresses have special chars in them
# encoding=utf8
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

import sys
if sys.version_info > (3,):
    long = int

    '''
    validates the timestamp provided.  Ensures it is within 7 days of current time and provides examples.
    :param msec:
    :return:
    '''
def validate_timestamp(msec):
    currentTime = long(time.time() * 1000)
    # number of centiseconds 1 week ago
    offset = 7 * 24 * 3600 * 1000
    if msec > currentTime:
        raise ValueError("Cannot provide a future time.  CurrentTime in milli-epoch is {}".format(currentTime))
    if currentTime - msec > offset:
        raise ValueError("timestamp greater than 7 days, time {}(milli-epoch)-> {}"
                         "\n 7 days ago would be {} milli-epoch".format(msec,
                                                            msec_to_time(msec),
                                                            (currentTime - msec)))

def utc_to_local(utc):
    gmTime = time.strptime(utc, '%Y-%m-%dT%H:%M:%S.%f+0000')
    ### convert to localtime
    localEpoc = calendar.timegm(gmTime)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(localEpoc))


def msec_to_time(msec):
    epoc = msec /1000
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoc))

def process_hosts(data):
    formatstr = '{:20s}{:15s}{:10s}{:16s}{:26s}{:10s}'
    print(formatstr.format("Device Family","Name", "Health", "IP Address", "Location", "allMetricValue"))

    for device in data:

        print(formatstr.format(
                               device['family'],
                               str(device['name'].split(".")[0]),
                               str(device['healthScore'][0]['score']),
                               str(device['managementIpAddress']),
                               str(device['location']),
                               str(device['allMetricValue'])

                               ))
def get_network_devices(raw):
    now = long(time.time() * 1000) - (300 * 1000)
    start = now - (300 * 1000)
    url = "api/assurance/v1/network-device?startTime={}&endTime={}".format(start,now)

    data = post(url, data={})
    if raw:
        print(json.dumps(data,indent=2))
    else:
        process_hosts(data['response'])

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')

    parser.add_argument('--raw', action='store_true',
                        help="raw json")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    get_network_devices(args.raw)