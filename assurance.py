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

def print_client_detail(data):
    conn = data['connectionInfo']
    print("Client Detail for:{} at {} ({})".format(conn['nwDeviceMac'],
                                                   msec_to_time(conn['timestamp']),
                                                   conn['timestamp']))
    print("HostType: {} connected to {}".format(conn['hostType'],conn['nwDeviceName']))

def print_network_health(data):
    print("Network Health")
def print_device_detail(data):
    print("Device Detail for {}".format(data['nwDeviceName']))
    print("Health:{}, cpuScore:{}, memoryScore{}".format(data['overallHealth'],
                                                         data['cpuScore'],
                                                         data['memoryScore']))
def print_client_health(data):
    print("Client health")

def print_site_health(data):
    print("Site Health")
    format_string="{:<20s}{:<10s}{:<8s}{:<14s}{:<14s}"
    print(format_string.format("SiteName","SiteType","Issues","RouterHealth", "AccessHealth"))

    for site in data:
        print(format_string.format(site['siteName'],
                                   site['siteType'],
                                   str(site['clientNumberOfIssues']),
                                   str(site['networkHealthRouter']),
                                   str(site['networkHealthAccess'])))

def print_formatted(data, israw):
    if israw:
        print(json.dumps(data,indent=2))
        return
    try:
        if "connectionInfo" in data:
            # client_detail
            print_client_detail(data)
        elif "latestMeasuredByEntity" in data:
            # network health
            print_network_health(data)
        elif "response" in data:
            body = data['response']
            if 'platformId' in body:
                #device detail
                print_device_detail(body)
            elif 'scoreDetail' in body[0]:
                # client health
                print_client_health(body)
            elif 'siteType' in body[0]:
                #site health
                print_site_health(body)
    except KeyError:
        print("No Valid data returned")




if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')

    parser.add_argument('--mac', type=str, required=False,
                        help="macAddress   e.g 00:26:08:E0:F4:97")
    parser.add_argument('--deviceName', type=str, required=False,
                        help="deviceName   e.g 3504")
    parser.add_argument('--timestamp', type=str, required=False, default='',
                        help="timestamp")
    parser.add_argument('--raw', action='store_true',
                        help="raw json")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    if args.timestamp:
        timestamp = long(args.timestamp)
        print ("Timestamp({}):{}".format(timestamp, msec_to_time(timestamp)))

    if args.mac:
        client_detail =  get_url('dna/intent/api/v1/client-detail?timestamp={}&macAddress={}'.format(args.timestamp, args.mac))
        print_formatted(client_detail, args.raw)
    elif args.deviceName:
        device_detail = get_url('dna/intent/api/v1/device-detail?timestamp={}&searchBy={}&identifier=nwDeviceName'.format(args.timestamp,args.deviceName))
        print_formatted(device_detail, args.raw)
    else:
        health = get_url('dna/intent/api/v1/site-health?timestamp={}'.format(args.timestamp))
        print_formatted(health,args.raw)
        client_health = get_url('dna/intent/api/v1/client-health?timestamp={}'.format(args.timestamp))
        print_formatted(client_health, args.raw)
        #start = long(client_health['response'][0]['scoreDetail'][0]['starttime'])
        #end = long(client_health['response'][0]['scoreDetail'][0]['endtime'])

        network_health = get_url('dna/intent/api/v1/network-health?timestamp={}'.format(args.timestamp))
        print_formatted(network_health, args.raw)



