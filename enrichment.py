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

    parser.add_argument('--mac', type=str, required=False,
                        help="macAddress   e.g 00:26:08:E0:F4:97")
    args = parser.parse_args()
    extraHeaders ={'entity_type': 'mac_address',
                   'entity_value' : args.mac}
    client_enrichment = get_url('dna/intent/api/v1/get-user-enrichment-details',extraHeaders=extraHeaders)
    print (json.dumps(client_enrichment, indent=2))