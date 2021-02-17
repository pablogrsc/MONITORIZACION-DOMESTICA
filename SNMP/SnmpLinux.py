import sys
import mysql.connector
import config
import datetime
import socket
import SnmpCpuLinux
import SnmpRamLinux
import SnmpStorageLinux


def insert_db(values):
        cn = mysql.connector.connect(host="127.0.0.1", database="homemonitor_db", user="pi", password="castellar", auth_plugin="mysql_native_password")
        sql_executer = cn.cursor()

        aql1 = "INSERT INTO snmp_linux (hour, hostname, load1, load5, load15, user_cpu, system_cpu, idle_cpu, ram_total, ram_free, ram_buffer, ram_cache, disk_total, disk_free, disk_used, disk_percent) VALUES ("
        aql2 = ""
        for i in range (len(values)):
            values[i] = "\"" + str(values[i]) + "\""
            if (i!=15):
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
    for i in range (len(config.linux_target_addresses)):
        cpu = SnmpCpuLinux.SnmpCpuLinux()
        ram = SnmpRamLinux.SnmpRamLinux()
        disk = SnmpStorageLinux.SnmpStorageLinux()

        cpu_value = cpu.monitor_cpu(config.linux_target_addresses[i], config.community)
        ram_value = ram.monitor_ram(config.linux_target_addresses[i], config.community)
        disk_value = disk.monitor_storage(config.linux_target_addresses[i], config.community)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostname = gethostname(config.linux_target_addresses[i])

        values = [time, hostname, str(cpu_value[0]), str(cpu_value[1]), str(cpu_value[2]), str(cpu_value[3]), str(cpu_value[4]), str(cpu_value[5]), str(ram_value[0]), str(ram_value[1]), str(ram_value[2]), str(ram_value[3]), str(disk_value[0]), str(disk_value[1]), str(disk_value[2]), str(disk_value[3])]

        insert_db(values)