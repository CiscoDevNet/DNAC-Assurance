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
    formatstr = '{:20s}{:10s}{:15s}{:10s}{:16s}{:20s}{:10s}{}'
    print(formatstr.format("id","Host Type","Host Name", "Health", "IP Address", "Location", "SSID","Link Speed"))

    for host in data:
        print(formatstr.format(host['id'],
                               host['hostType'],
                               str(host['hostName']),
                               str(host['healthScore'][0]['score']),
                               str(host['hostIpV4']),
                               host['location'],
                               str(host['ssid']),
                               host['linkSpeed']
                               ))
def get_hosts(raw, wired, wireless):
    url = "api/assurance/v1/host"
    payload = {}
    if wired:
        payload['filters']= {"devType": ["WIRED"]}
    if wireless:
        payload['filters']= {"devType": ["WIRELESS"]}
    data = post(url, data=payload)
    if raw:
        print(json.dumps(data,indent=2))
    else:
        process_hosts(data['response'])

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')


    parser.add_argument('--raw', action='store_true',
                        help="raw json")
    parser.add_argument('--wired', action='store_true',
                        help="wired clients only")
    parser.add_argument('--wireless', action='store_true',
                        help="wireless clients only")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    get_hosts(args.raw, args.wired, args.wireless)