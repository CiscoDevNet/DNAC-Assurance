#!/usr/bin/env python

from __future__ import print_function
import json
import logging
import time
import calendar
from datetime import datetime
from argparse import ArgumentParser
from util import get_url, post_and_wait
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

def find_node(nodes, nodeId):
    for node in nodes:
        if node['id'] == nodeId:
            return node
    print("no node found")
    raise KeyError("Cannot find nodeId:{}",nodeId)

def print_node(node):
    if node['role'] == 'Client':
        return '{}({})[{}] - Health:{}'.format(node['ip'],
                                              node['userId'],
                                              node['deviceType'],
                                              node['healthScore'])
    elif node['role'] == 'SSID':
        return 'SSID: {}({})'.format(node['name'],
                                     node['radioFrequency'])
    elif node['role'] == 'ACCESS':
        return '{}:{}:{}({}) - Health:{}'.format(node['name'],
                                                       node['ip'],
                                                       node['platformId'],
                                            node['softwareVersion'],
                                             node['healthScore'])
    else:
        return (str(node))

def print_topology(topo):

    destNode = None
    for link in topo['links']:
        sourceNode = find_node(topo['nodes'], link['source'])

        destNode = find_node(topo['nodes'], link['target'])

        print('{} ->'.format(print_node(sourceNode)))
    if destNode is not None:
        print(print_node(destNode))

def print_client_detail(data):
    detail = data['detail']
    print("Client Detail for:{} at {} ({})".format(detail['hostMac'],
                                                   msec_to_time(detail['lastUpdated']),
                                                   detail['lastUpdated']))
    ### new code
    # extra WLAN info
    if detail['hostType'] == 'WIRELESS':
        wlan = '[ frequency:{}, channel:{}, ssid:{}, rssi:{}]'.format(detail['frequency'],
                                                                         detail['channel'],
                                                                         detail['ssid'],
                                                                         detail['rssi'])
    else:
        wlan = ''

    print("HostType: {} connected to {} {}\n".format(detail['hostType'],detail['hostName'], wlan))
    print_topology(data['topology'])

def print_network_health(data):

    try:
        print("Network Health: {}% at {}".format(data['response'][0]['healthScore'], utc_to_local(data['response'][0]['time'])))
    except IndexError:
        print("No data received")
        return
    print("\n Devices Monitored {}, unMonitored {}".format(data['monitoredDevices'], data['unMonitoredDevices']))
    format_string="{:<11s}{:<10s}{:<10s}{}"
    print(format_string.format("Category", 'Score', 'Good%','KPI'))
    for category in data['healthDistirubution']:
        #print(json.dumps(category, indent=2))
        kpi = ''
        if 'kpiMetrics' in category:
            kpis = ['{}:{}'.format(k['key'], k['value']) for k in category['kpiMetrics'] ]
            if kpis:
                kpi = ','.join(kpis)

        print(format_string.format(' ' +category['category'],
                                   str(category['healthScore']),
                                   str(round(category['goodPercentage'],1)),
                                kpi))

def print_device_detail(data):
    print("Device Detail for {}".format(data['nwDeviceName']))
    print("Type:{}, OS Version:{}".format(data['nwDeviceType'],data['softwareVersion']))
    print("Health:{}, cpuScore:{}, memoryScore:{}".format(data['overallHealth'],
                                                         data['cpuScore'],
                                                        data['memoryScore']))
def process_score(score):
    #print(json.dumps(score, indent=2))
    print(score['scoreCategory']['value'], score['clientCount'])
    if 'scoreList' in score:

        for entry in score['scoreList']:
            print(" {} ({}) ".format(entry['scoreCategory']['value'], entry['clientCount']), end='')
            #print(json.dumps(entry,indent=2))
            if 'scoreList' in entry:
                for item in entry['scoreList']:
                    if "ALL" in item['scoreCategory']['value']:
                        continue
                    print("{}:{}({})".format(item['scoreCategory']['scoreCategory'],
                                      item['scoreCategory']['value'],
                                      item['clientCount']),end='')
            print()

def print_client_health(data):

    try:
        start = long(client_health['response'][0]['scoreDetail'][0]['starttime'])
        end = long(client_health['response'][0]['scoreDetail'][0]['endtime'])
    except KeyError:
        print("No time found")

    print("Client health @ {} <-> {} ({}-{})".format(msec_to_time(start),msec_to_time(end),start,end))

    for score in data[0]['scoreDetail']:
        #print(json.dumps(score,indent=2))
        process_score(score)

def print_site_health(data):
    print("Site Health")
    format_string=u"{:<20s}{:<10s}{:<8s}{:<14s}{:<14s}{:<14s}{:<14s}"
    print(format_string.format("SiteName","SiteType","Issues","RouterHealth", "AccessHealth", "ClientHealth", "ClientCount"))

    for site in data:
        print(format_string.format(site['siteName'],
                                   site['siteType'],
                                   # seems broken in 1.3
                                   #str(site['clientNumberOfIssues']),
                                   "0",
                                   str(site['networkHealthRouter']),
                                   str(site['networkHealthAccess']),
                                   str(site['healthyClientsPercentage']),
                                   str(site['numberOfClients'])))

def print_formatted(data, israw):
    if israw:
        print(json.dumps(data,indent=2))
        return
    try:
        if "detail" in data:
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
    except KeyError as e:
        print("No Valid data returned:{}".format(e.message))
        print(data.keys())
    print('\n')



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
        validate_timestamp(timestamp)
        print ("Timestamp({}):{}".format(timestamp, msec_to_time(timestamp)))

    if args.mac:
        # client detail needs timestamp
        if not args.timestamp:
            # take 5mins ago by default
            clientTimestamp = (long(time.time()) * 1000) - 3000000
        else:
            clientTimestamp = args.timestamp
        client_detail =  get_url('dna/intent/api/v1/client-detail?timestamp={}&macAddress={}'.format(clientTimestamp, args.mac))
        print_formatted(client_detail, args.raw)
    elif args.deviceName:
        # client detail needs timestamp
        if not args.timestamp:
            # take 5mins ago by default
            clientTimestamp = (long(time.time()) * 1000) - 3000000
        else:
            clientTimestamp = args.timestamp
        device_detail = get_url('dna/intent/api/v1/device-detail?timestamp={}&searchBy={}&identifier=nwDeviceName'.format(clientTimestamp,args.deviceName))
        print_formatted(device_detail, args.raw)
    else:
        health = get_url('dna/intent/api/v1/site-health?timestamp={}'.format(args.timestamp))
        print_formatted(health,args.raw)

        ## need to provide a timestamp for client-health
        if not args.timestamp:
            clientTimestamp = long(time.time()) * 1000
        else:
            clientTimestamp = args.timestamp

        client_health = get_url('dna/intent/api/v1/client-health?timestamp={}'.format(clientTimestamp))
        print_formatted(client_health, args.raw)

        network_health = get_url('dna/intent/api/v1/network-health?timestamp={}'.format(args.timestamp))
        print_formatted(network_health, args.raw)



