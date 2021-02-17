#!/usr/bin/env python

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import config

class SnmpCpuLinux():
    def __init__(self):
        self.snmp_ois = {
            'userCpu': '1.3.6.1.4.1.2021.11.9.0',
            'systemCpu': '1.3.6.1.4.1.2021.11.10.0',
            'idleCpu': '1.3.6.1.4.1.2021.11.11.0',
            'load1': '1.3.6.1.4.1.2021.10.1.3.1',
            'load5': '1.3.6.1.4.1.2021.10.1.3.2',
            'load15': '1.3.6.1.4.1.2021.10.1.3.3',
        }
        self.port=161
        self.cpu = []

    def get_value(self, list, value):
        for name, val in list:
            if str(name) == value:
                return float(val)
        return None

    def monitor_cpu(self, host, community):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community),
                cmdgen.UdpTransportTarget((host, self.port)),
                self.snmp_ois.get('userCpu'),
                self.snmp_ois.get('systemCpu'),
                self.snmp_ois.get('idleCpu'),
                self.snmp_ois.get('load1'),
                self.snmp_ois.get('load5'),
                self.snmp_ois.get('load15'),
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
                load1 = self.get_value(varBinds, self.snmp_ois.get('load1'))*100/4
                load5 = self.get_value(varBinds, self.snmp_ois.get('load5'))*100/4
                load15 = self.get_value(varBinds, self.snmp_ois.get('load15'))*100/4
                userCpu = self.get_value(varBinds, self.snmp_ois.get('userCpu'))
                systemCpu = self.get_value(varBinds, self.snmp_ois.get('systemCpu'))
                idleCpu = self.get_value(varBinds, self.snmp_ois.get('idleCpu'))

                print ('Cpu Load over the last minutes: 1 minute last: {0}% - 5 minutes last: {1}% - 15 minutes last: {2}%'.format(
                    load1,
                    load5,
                    load15,
                ));
                print('Cpu Usage over last minute; User Usage: {0:.2}% - System Usage: {1:.2}% - Idle Time: {2:.2f}%'.format(
                    userCpu,
                    systemCpu,
                    idleCpu,
                ));

        self.cpu = [load1, load5, load15, userCpu, systemCpu, idleCpu]
        return self.cpu

#On a multi-processor system, the 'ssCpuRaw*'
#counters are cumulative over all CPUs, so their
#sum will typically be N*100 (for N processors). -> X ESO EL /4
#

#if __name__ == '__main__':
#    monitor = SnmpCpuLinux()
#    monitor.monitor_cpu(config.target_address, config.community)