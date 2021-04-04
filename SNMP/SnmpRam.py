#!/usr/bin/env python

import config
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

class SnmpRam():
    def __init__(self):
        self.snmp_ois = {
        'ram': '1.3.6.1.2.1.25.2.2.0',
        'ram_used' : '1.3.6.1.2.1.25.2.3.1.6.',
        'allocation' : '1.3.6.1.2.1.25.2.3.1.4.'
        }
        self.port=161
        self.ram = 0
        self.cont=0

    def get_value(self, list, value):
        for name, val in list:
            if str(name) == value:
                return float(val)
        return None

    def is_partition(self, list, value):
        for name,val in list:
            if (format(val) is not ''):
                return True
            else:
                return False

    def count_partition(self, host, community):
        i=1
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(community),
            cmdgen.UdpTransportTarget((host, self.port)),
            self.snmp_ois.get('ram_used')+str(i),
            self.snmp_ois.get('allocation') + str(i)
            )
        while (self.is_partition(varBinds, self.snmp_ois.get('ram_used') + str(i))):
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('ram_used')+str(i),
                self.snmp_ois.get('allocation') + str(i)
                )
            i=i+1
            self.cont=self.cont+1

    def monitor_ram(self, host, community):
        self.count_partition(host, community)
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('ram'),
                self.snmp_ois.get('ram_used')+str(self.cont-1),
                self.snmp_ois.get('allocation')+str(self.cont-1)
        )
        if errorIndication:
            print("ERROR1: %s" % errorIndication)
        else:
            if errorStatus:
                print('ERROR2: %s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                total_ram = self.get_value(varBinds, self.snmp_ois.get('ram'))
                used_ram = self.get_value(varBinds, self.snmp_ois.get('ram_used')+str(self.cont-1)) * self.get_value(varBinds, self.snmp_ois.get('allocation')+str(self.cont-1))
                print("The total RAM of the host is: {0:.3f}GB".format(total_ram/pow(1024,2)))
                print("The used RAM of the host is: {0:.3f}GB".format(used_ram/pow(1024,3)))
                self.ram = [(total_ram/pow(1024,2)), (used_ram/pow(1024,3))]
        return self.ram

#if __name__ == '__main__':
#    monitor = SnmpRam()
#    monitor.monitor_ram('192.168.1.50', config.community)