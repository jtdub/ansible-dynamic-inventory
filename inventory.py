#!/usr/bin/env python

import yaml
import os
import sys
import argparse
import json


class Inventory(object):

    def __init__(self):
        self.inventory = dict()
        self.arguments()

        if self.args.host:
            self.inventory = self._build_inventory(host=self.args.host)
        else:
            self.inventory = self._build_inventory(host='all')

        print(self.inventory)

    def arguments(self):
        parser = argparse.ArgumentParser(
            description='Ansible Inventory for Rackspace DNS Infrastructure')
        parser.add_argument('--list',
                            help='List all devices in inventory',
                            nargs='?',
                            const=True)
        parser.add_argument('--host',
                            help='List a specific device in inventory')
        parser.add_argument('-p', '--pretty',
                            help='Make inventory output pretty.',
                            nargs='?',
                            const=True)
        self.args = parser.parse_args()

    def _build_inventory(self, host):
        global_inv = dict()
        global_inv['_meta'] = dict()
        global_inv['_meta']['hostvars'] = dict()

        if host == 'all':
            hosts = os.listdir('host_vars')
            global_inv['all'] = hosts
        else:
            if os.path.isfile('host_vars/{}'.format(host)):
                hosts = [host]
                global_inv['all'] = hosts
            else:
                print('Error: hostvars for {} does not exist.'.format(host))
                sys.exit(1)

        for host in hosts:
            host_inv = yaml.load(open('host_vars/{}'.format(host)))
            global_inv['_meta']['hostvars'][host] = dict()
            if len(host_inv) > 0:
                if 'groups' in host_inv:
                    for item in host_inv['groups']:
                        if item in global_inv:
                            if host not in global_inv[item]:
                                global_inv[item].append(host)
                        else:
                            global_inv[item] = list()
                            global_inv[item].append(host)

        if self.args.pretty:
            return json.dumps(global_inv, indent=2)
        else:
            return json.dumps(global_inv)


if __name__ == "__main__":
    Inventory()
