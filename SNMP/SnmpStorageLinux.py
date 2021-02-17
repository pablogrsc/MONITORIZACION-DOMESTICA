#!/usr/bin/env python

import sys
import config
from pysnmp.entity.rfc3413.oneliner import cmdgen

class SnmpStorageLinux():
    def __init__(self):
        self.snmp_ois = {
            'total': '1.3.6.1.4.1.2021.9.1.6.1',
            'free': '1.3.6.1.4.1.2021.9.1.7.1',
            'used': '1.3.6.1.4.1.2021.9.1.8.1',
            'percentused': '1.3.6.1.4.1.2021.9.1.9.1',
        }
        self.port=161
        self.disk = []

    def get_value(self, list, value):
        for name, val in list:
            if str(name) == value:
                return float(val)
        return None

    def monitor_storage(self, host, community):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('total'),
                self.snmp_ois.get('free'),
                self.snmp_ois.get('used'),
                self.snmp_ois.get('percentused')
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
                disk_total = float(self.get_value(varBinds, self.snmp_ois.get('total'))) / pow(1024,2) * 1.074
                disk_free = float(self.get_value(varBinds, self.snmp_ois.get('free')))  / pow(1024,2) * 1.074
                disk_used = float(self.get_value(varBinds, self.snmp_ois.get('used'))) / pow(1024,2) * 1.074
                disk_percentused = float(self.get_value(varBinds, self.snmp_ois.get('percentused')))

                print('Space for Linux System on the host; Total: {0:.2f}GB - Free: {1:.2f}GB - Used: {2:.2f}GB - Percent of Used Disk: {3:.2f}%'.format(
                    disk_total,
                    disk_free,
                    disk_used,
                    disk_percentused
                    )
                );
        self.disk = [disk_total, disk_free, disk_used, disk_percentused]
        return self.disk;


if __name__ == '__main__':
    monitor = SnmpStorageLinux()
    monitor.monitor_storage(config.target_address, config.community)