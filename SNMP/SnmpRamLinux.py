#!/usr/bin/env python

import sys
import config
from pysnmp.entity.rfc3413.oneliner import cmdgen

class SnmpRamLinux():
    def __init__(self):
        self.snmp_ois = {
            'total': '1.3.6.1.4.1.2021.4.5.0',
            'free': '1.3.6.1.4.1.2021.4.6.0',
            'buffer': '1.3.6.1.4.1.2021.4.14.0',
            'cache': '1.3.6.1.4.1.2021.4.15.0',
        }
        self.port=161
        self.ram = []

    def get_value(self, list, value):
        for name, val in list:
            if str(name) == value:
                return float(val)
        return None

    def monitor_ram(self, host, community):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('total'),
                self.snmp_ois.get('free'),
                self.snmp_ois.get('buffer'),
                self.snmp_ois.get('cache')
        )
        if errorIndication:
            print("ERROR1: %s" % errorIndication)
            sys.exit(1)
        else:
            if errorStatus:
                print('ERROR2: %s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
                sys.exit(1)
            else:
                total_ram = float(self.get_value(varBinds, self.snmp_ois.get('total')) / pow(1024,2) * 1.074)
                free_ram = float(self.get_value(varBinds, self.snmp_ois.get('free')) / pow(1024,2) * 1.074)
                cache_ram = float(self.get_value(varBinds, self.snmp_ois.get('cache')) / pow(1024,2) * 1.074)
                used_ram = total_ram - free_ram - cache_ram
                percent_ram = (used_ram / total_ram ) * 100

                print('Space Ram of the Host: Total: {0:.2f}GB - Free: {1:.2f}GB - Cache: {2:.2f}GB - Percent of Used Ram: {3:.2f}%'.format(
                    total_ram,
                    free_ram,
                    cache_ram,
                    percent_ram
                    )
                );
        self.ram = [total_ram, free_ram, cache_ram, used_ram, percent_ram]
        return self.ram

#if __name__ == '__main__':
#    monitor = SnmpRamLinux()
#    monitor.monitor_ram(config.target_address, config.community)