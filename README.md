# Ansible Dynamic Inventory 
## Gleaning Dynamic Inventory from host_vars and group_vars

Creating INI style static inventory files isn't any fun. This script reads the devices from the host_vars file and creates an Ansible inventory dynamically.
Groups are assigned in the host_vars yaml file. For example in the 'router1' file you have:
```yaml
---
groups:
- os_ios
- routers

interfaces:
  FastEthernet0:
    ipv4_address: 10.0.0.1 255.255.255.0
```

The 'groups' yaml syntax assigns the router1 device to the os_ios and routers groups. From there, ansible will automatically inherit the variables from those groups into the router1 inventory.

Here is an example ansible-playbook run:

```
$ ansible-playbook -i inventory.py playbooks/test.yml --limit router1

PLAY [all] ********************************************************************

TASK: [DISPLAY INVENTORY VARIABLES] *******************************************
ok: [router1] => {
    "var": {
        "hostvars": {
            "domain": "example.com",
            "group_names": [
                "os_ios",
                "routers"
            ],
            "groups": {
                "all": [
                    "switch1",
                    "router1"
                ],
                "os_ios": [
                    "router1",
                    "switch1"
                ],
                "routers": [
                    "router1"
                ],
                "switches": [
                    "switch1"
                ]
            },
            "interfaces": {
                "FastEthernet0": {
                    "ipv4_address": "10.0.0.1 255.255.255.0"
                }
            },
            "inventory_hostname": "router1",
            "inventory_hostname_short": "router1",
            "layer": 3
        }
    }
}

PLAY RECAP ********************************************************************
router1                    : ok=1    changed=0    unreachable=0    failed=0
```

Here is what executing the inventory.py script independently renders:

```
$ ./inventory.py --help
usage: inventory.py [-h] [--list [LIST]] [--host HOST] [-p [PRETTY]]

Ansible Inventory for Rackspace DNS Infrastructure

optional arguments:
  -h, --help            show this help message and exit
  --list [LIST]         List all devices in inventory
  --host HOST           List a specific device in inventory
  -p [PRETTY], --pretty [PRETTY]
                        Make inventory output pretty.

$ ./inventory.py -p
{
  "switches": [
    "switch1"
  ],
  "os_ios": [
    "router1",
    "switch1"
  ],
  "all": [
    "router1",
    "switch1"
  ],
  "_meta": {
    "hostvars": {
      "switch1": {},
      "router1": {}
    }
  },
  "routers": [
    "router1"
  ]
}
```
