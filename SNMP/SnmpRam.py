#!/usr/bin/env python

import config
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

class SnmpRam():
    def __init__(self):
        self.snmp_ois = {'ram': '1.3.6.1.2.1.25.2.2.0'}
        self.port=161
        self.ram = 0

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
                self.snmp_ois.get('ram')
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
                print("The total RAM of the host is: {0:.3f}GB".format(total_ram/pow(1024,2)))
                self.ram = (total_ram/pow(1024,2))
        return self.ram

#if __name__ == '__main__':
#    monitor = SnmpRam()
#    monitor.monitor_ram(config.target_address, config.community)