import sys
import mysql.connector
import config
import datetime
import socket
import SnmpCpu
import SnmpRam
import SnmpStorage


def insert_db(values):
        cn = mysql.connector.connect(host="127.0.0.1", database="homemonitor_db", user="XXX", password="XXX", auth_plugin="mysql_native_password")
        sql_executer = cn.cursor()

        aql1 = "INSERT INTO snmp_windows (hour, hostname, cpu_usage, ram_total, disk_total, disk_used, disk_free, disk_percent) VALUES ("
        aql2 = ""
        for i in range (len(values)):
            values[i] = "\"" + str(values[i]) + "\""
            if (i!=7):
                values[i] += ","
            aql2 = aql2 + values[i]
        aql = aql1 + aql2 + ");"
        print (aql)
        sql_executer.execute(aql)
        cn.commit()

def gethostname(ip):
    try:
        hostname = socket.getfqdn(ip)
    except (socket.error, socket.herror, socket.gaierror) as e:
        hostname = "Unknown"

    if (hostname == ip):
        return "Unknown"
    else:
        return hostname

if __name__ == '__main__':
    for i in range (len(config.windows_target_addresses)):
        cpu = SnmpCpu.SnmpCpu()
        ram = SnmpRam.SnmpRam()
        disk = SnmpStorage.SnmpStorage()
        ram_value = ram.monitor_ram(config.windows_target_addresses[i], config.community)
        disk_value = disk.monitor_storage(config.windows_target_addresses[i], config.community)
        cpu_value = cpu.monitor_cpu(config.windows_target_addresses[i], config.community)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostname = gethostname(config.windows_target_addresses[i])

        values = [time, hostname, str(cpu_value), str(ram_value), str(disk_value[0]), str(disk_value[1]), str(disk_value[2]), str(disk_value[3])]

        insert_db(values)
