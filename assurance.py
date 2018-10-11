#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import logging
import time
from argparse import ArgumentParser
from util import get_url, post_and_wait

def show_templates():
    print("Available Templates:")
    result = get_url("template-programmer/template")
    print ('\n'.join(sorted([ '  {0}/{1}'.format(project['projectName'], project['name']) for project in result])))
    #for project in result:
    #    print( '{0}/{1}'.format(project['projectName'], project['name']))


def msec_to_time(msec):
    epoc = msec /1000
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoc))


if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')

    parser.add_argument('--mac', type=str, required=False,
                        help="macAddress   e.g 00:26:08:E0:F4:97")
    parser.add_argument('--deviceName', type=str, required=False,
                        help="deviceName   e.g 3504")
    parser.add_argument('--timestamp', type=str, required=False, default='',
                        help="timestamp")

    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    site_health = get_url('dna/intent/api/v1/site-health?timestamp={}'.format(args.timestamp))
    print (json.dumps(site_health, indent=2))
    device_detail = get_url('dna/intent/api/v1/device-detail?timestamp={}&searchBy={}&identifier=nwDeviceName'.format(args.timestamp,args.deviceName))
    print(json.dumps(device_detail, indent=2))
    client_health = get_url('dna/intent/api/v1/client-health?timestamp={}'.format(args.timestamp))
    print(json.dumps(client_health, indent=2))
    start = long(client_health['response'][0]['scoreDetail'][0]['starttime'])
    end = long(client_health['response'][0]['scoreDetail'][0]['endtime'])
    client_detail = get_url('dna/intent/api/v1/client-detail?timestamp={}&macAddress={}'.format(args.timestamp, args.mac))
    print(json.dumps(client_detail, indent=2))



    if args.timestamp:
        timestamp = long(args.timestamp)
        #print  (timestamp - start)
        #print (end - timestamp)
        print ("Start", msec_to_time(start), "Timestamp", msec_to_time(timestamp), "End", msec_to_time(end))

