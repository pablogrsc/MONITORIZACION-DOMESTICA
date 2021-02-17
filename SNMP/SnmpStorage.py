#!/usr/bin/env python

import sys
import config
from pysnmp.entity.rfc3413.oneliner import cmdgen

class SnmpStorage():
    def __init__(self):
        self.snmp_ois = {
            'total': '1.3.6.1.2.1.25.2.3.1.5.',
            'used': '1.3.6.1.2.1.25.2.3.1.6.',
            'allocation': '1.3.6.1.2.1.25.2.3.1.4.',
        }
        self.port=161
        self.total=0
        self.used=0

    def get_value(self, list, value):
        for name, val in list:
            if str(name) == value:
                return float(val)
        return None

    def count_partition(self, list, value):
        for name,val in list:
            if (format(val) != None):
                return True
            else:
                return False

    def monitor_storage(self, host, community):
        i=1
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('total') + str(i),
                self.snmp_ois.get('used') + str(i),
                self.snmp_ois.get('allocation') + str(i)
        )
        while(self.count_partition(varBinds, self.snmp_ois.get('total') + str(i))):
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('total') + str(i),
                self.snmp_ois.get('used') + str(i),
                self.snmp_ois.get('allocation') + str(i)
            )
            if errorIndication:
                #print("ERROR1: %s" % errorIndication)
                break
            else:
                if errorStatus:
                    #print('ERROR2: %s at %s' % (
                    #    errorStatus.prettyPrint(),
                    #    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    #    )
                    #)
                    break
                else:
                        self.total = self.total + self.get_value(varBinds, self.snmp_ois.get('total')+str(i)) * self.get_value(varBinds, self.snmp_ois.get('allocation')+str(i))
                        self.used = self.used + self.get_value(varBinds, self.snmp_ois.get('used')+str(i)) * self.get_value(varBinds, self.snmp_ois.get('allocation')+str(i))
                        i=i+1
        free = self.total - self.used
        print("Space of the host disk is:")
        print("\tTotal: {0:.4f}GB".format(self.total / pow(1024,3)))
        print("\tUsed: {0:.4f}GB".format(self.used / pow(1024,3)))
        print("\tFree: {0:.4f}GB".format(free / pow(1024,3)))
        print("\tPercentage of used Disk: {0:.2f}%".format(((self.used*100)/self.total)))
        disk = [self.total / pow(1024,3), self.used / pow(1024,3), free / pow(1024,3), ((self.used*100)/self.total)]
        return disk

#if __name__ == '__main__':
#    monitor = SnmpStorage()
#