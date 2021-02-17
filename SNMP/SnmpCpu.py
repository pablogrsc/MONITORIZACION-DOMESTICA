#!/usr/bin/env python

import sys
import config
from pysnmp.entity.rfc3413.oneliner import cmdgen
import mysql.connector

class SnmpCpu():
    def __init__(self):
        self.snmp_ois = {'cpu': '1.3.6.1.2.1.25.3.3.1.2.'}
        self.port=161
        self.cpu = 0

    def get_value(self, list, value):
        for name, val in list:
            if str(name) == value:
                return float(val)
        return None

    def count_cores(self, list, value):
        for name,val in list:
            if (format(val) != None):
                return True
            else:
                return False

    def monitor_cpu(self, host, community):
        i=8
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('cpu') + str(i),
        )
        while(self.count_cores(varBinds, self.snmp_ois.get('cpu') + str(i))):
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('cpu') + str(i),
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
                    cpu_usage = self.get_value(varBinds, self.snmp_ois.get('cpu')+str(i))
                    self.cpu += cpu_usage
                    print("The percentage of work time of Core{0} in the last minute was {1}%".format(i-7, cpu_usage))
                    i=i+1
        return self.cpu/(i-8)