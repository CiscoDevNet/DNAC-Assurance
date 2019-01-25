#!/usr/bin/env python

from __future__ import print_function
import json
import logging
import time
import calendar
from datetime import datetime
from argparse import ArgumentParser
from util import get_url, post_and_wait

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')

    parser.add_argument('--mac_address', type=str, required=False,
                        help="macAddress   e.g 00:26:08:E0:F4:97")
    parser.add_argument('--network_user_id', type=str, required=False,
                        help="network user id   e.g adam")
    parser.add_argument('--ip_address', type=str, required=False,
                        help="ip address   e.g 10.10.10.10")
    parser.add_argument('--etype', type=str, required=False, default="user",
                        help="type - client, user, device, issue")
    args = parser.parse_args()

    if args.mac_address:
        extraHeaders ={'entity_type': 'mac_address',
                   'entity_value' : args.mac_address}
    elif args.network_user_id:
        extraHeaders = {'entity_type': 'network_user_id',
                        'entity_value': args.network_user_id}
    elif args.ip_address:
        extraHeaders = {'entity_type': 'ip_address',
                        'entity_value': args.ip_address}

    enrichment_data = get_url('dna/intent/api/v1/{}-enrichment-details'.format(args.etype),extraHeaders=extraHeaders)
    print (json.dumps(enrichment_data, indent=2))