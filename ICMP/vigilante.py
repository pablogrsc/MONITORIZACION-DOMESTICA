#!/usr/bin/env python3
import time
import subprocess
import re
import json
import os
import requests
import socket
import math
import sys
import mysql.connector
from multiprocessing import Process, Manager


class Vigilante():
    def __init__(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(self.dir, 'vigilante.json') #ruta del archivo json donde vuelca los datos
        self.read_keys()
        self.local_ip = self.get_local_ip() #coge ip privada de la raspberry
        self.manager = Manager() #Manager() crea procesos (hilos) concurrentemente

        if os.path.exists(self.filename):
            self.read()
        else:
            self.ips = []
            self.macs = {}
            self.save()

    def get_mac_address(self, ip):
        try:
            proc = subprocess.Popen(['arp', '-n', ip], stdout=subprocess.PIPE)
            out, err = proc.communicate()
            ans = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', out.decode(), re.I).group()
        except:
            ans = 'Unknown'
        return ans

    def get_local_ip(self):
        proc = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
        out, err = proc.communicate()
        return out.decode().split(' ')[0]

    def read_keys(self):
        filename = os.path.join('/home/pi/Desktop/Monitoring', 'keys.json')
        f = open(filename, 'r')
        content = f.read()
        f.close()
        data = json.loads(content)
        self.token = data['token']
        self.channel_id = data['channel_id']

    def send_warning(self, message):
        url = 'https://api.telegram.org/bot{0}/sendMessage'.format(self.token)
        data = {'chat_id': self.channel_id, 'text': message}
        r = requests.post(url, data)

    def insert_db(self, values):
        cn = mysql.connector.connect(host="127.0.0.1", database="xx", user="xx", password="xx", auth_plugin="mysql_native_password")
        sql_executer = cn.cursor()

        aql1 = "INSERT INTO hosts (hostname, ip, mac) VALUES ("
        aql2 = ""
        for i in range (len(values)):
            values[i] = "\"" + str(values[i]) + "\""
            if (i!=2):
                values[i] += ","
            aql2 = aql2 + values[i]
        aql = aql1 + aql2 + ");"

        print (aql)
        sql_executer.execute(aql)
        cn.commit()

    def read(self):
        f = open(self.filename, 'r')
        content = f.read()
        f.close()
        data = json.loads(content)
        self.macs = data['macs']
        self.ips = data['ips']

    def save(self):
        f = open(self.filename, 'w')
        data = {'macs': self.macs, 'ips': self.ips}
        f.write(json.dumps(data))

    def exists(self, item):
        if item.find(':') > -1:
            return mac in self.macs
        else:
            return ip in self.ips

    def add(self, item):
        if type(item) == dict:
            self.macs.append(item)
        else:
            self.ips.append(item)

    def check_host(self, ip):
        ret_code = subprocess.call(['ping', '-c1', '-W20', ip],
                                   stdout=subprocess.PIPE)
        if ret_code == 0:
            self.data[ip] = self.get_mac_address(ip)

    def vigila(self):
        self.data = self.manager.dict() #self.data es un diccionario compartido entre todos los procesos que cree manager.
        jobs = []
        range_ip = '.'.join(self.local_ip.split('.')[:-1]) #range_ip = 192.168.1
        for i in range(1, 255): #254
            ip = '{0}.{1}'.format(range_ip, i) #ip = 192.168.1.1 - 192.168.1.255
            if self.local_ip != ip:
                job = Process(target=self.check_host, args=(ip,))
                jobs.append(job)
                job.start()
        for job in jobs:
            job.join()
        for ip in self.data.keys():

            try:
                self.hostname = socket.getfqdn(ip)
            except (socket.error, socket.herror, socket.gaierror) as e:
                self.hostname = "Unknown"

            if (self.hostname == ip):
                self.hostname = "Unknown"

            if self.data[ip] == 'Unknown':
                if ip not in self.ips:
                    self.ips.append(ip)
                    message = "New device called {0} with IP {1} and MAC {2}".format(self.hostname, ip, str(self.data[ip]))
                    #message = "New device with IP {0} and MAC {1}".format(ip, self.data[ip])
                    self.send_warning(message)
                    values = [self.hostname,ip,str(self.data[ip])]
                    self.insert_db(values)
            else:
                if self.data[ip] not in self.macs.keys(): #Si es una
                    self.macs[self.data[ip]] = {'last_viewed': math.trunc(time.time()), 'in': True }
                    message = "New device called {0} with IP {1} and MAC {2}".format(self.hostname, ip, str(self.data[ip]))
                    #message = "New device with IP {0} and MAC {1}".format(ip, self.data[ip])
                    self.send_warning(message)
                    values = [self.hostname,ip,str(self.data[ip])]
                    self.insert_db(values)
                else:
                    if self.data[ip] in self.macs.keys():
                        if self.macs[self.data[ip]]['in'] is False:
                            message = self.hostname + '[' + str(self.data[ip]) + "] is back"
                            #message = "MAC " + str(self.data[ip]) + " is back"
                            self.send_warning(message)
                    self.macs[self.data[ip]] = {'last_viewed': math.trunc(time.time()), 'in': True}
        for mac in self.macs.keys():
            #if self.macs[mac]['last_viewed'] - time.time() > 30 * 60 and self.macs[mac]['in'] is True:
            if math.trunc(time.time()) - self.macs[mac]['last_viewed'] > 30 * 60 and self.macs[mac]['in'] is True:
                self.macs[mac]['in'] = False
                message = self.hostname + '[' + str(self.data[ip]) + "] is gone"
                #message = "MAC " + str(mac) + " is gone"
                self.send_warning(message)

if __name__ == '__main__':
    start = time.time()
    vigilante = Vigilante()
    vigilante.vigila()
    vigilante.save()
    print('Total time: {0}'.format(time.time() - start))
