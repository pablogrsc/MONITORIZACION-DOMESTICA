#!/usr/bin/env python

import json, math, random
from datetime import datetime
from re import search
import os
import requests
import config
import mysql.connector

PING_SERVERS = [
    '1.1.1.1',
    '1.0.0.1',
    '8.8.8.8',
    '8.8.4.4',
]

class ISPMonitor():
    def __init__(self):
        self.read_keys()


    def get_uptime(self):
        if self.is_online():
            now = int(datetime.now().strftime('%s'))
            with open(config.base_path + '/uptime.log', 'a+') as file:
                file.write('%d\n' % now)
                file.seek(0)
                timestamp = file.readline()
            first_online_timestamp = - now if timestamp == '' else int(timestamp)
            uptime = (now - first_online_timestamp) / (60 * 60)
            return '%d %s' % (uptime, 'hora' if uptime == 1 else 'horas')
        else:
            with open(config.base_path + '/uptime.log', 'w') as file:
                file.write('')
            raise Exception('There is no Internet connectivity')


    def is_online(self):
        self.write('Testing connectivity')
        for _ in range(10):
            ip = random.choice(PING_SERVERS)
            if os.system(f'ping {ip} -c 1 -W 5') == 0:
                return True
        return False


    def run_test(self):
        self.write('Running SpeedTest')
        print (config.base_path + '/results.log')
        os.system('speedtest --json > ' + config.base_path + '/results.log')


    def parse_results(self):
        self.write('Parsing Results')
        with open(config.base_path + '/results.log') as file:
            data = json.loads(file.read())
        return (
            [data['server']['latency'],
            data['download'] / 1048576,
            data['download'] / 1048576 /config.down_speed,
            data['upload'] / 1048576,
            data['upload'] / 1048576/ config.up_speed,
            data['server']['url']]
        )

    def read_keys(self):
        filename = os.path.join('/home/pi/Desktop/Monitoring', 'keys.json')
        f = open(filename, 'r')
        content = f.read()
        f.close()
        data = json.loads(content)
        self.token = data['token']
        self.channel_id = data['channel_id']

    def send_warning(self, uptime, results):
        url = 'https://api.telegram.org/bot{0}/sendMessage'.format(self.token)
        data = {'chat_id': self.channel_id, 'text': self.mount_status(uptime,results)}
        r = requests.post(url, data)

    def mount_status(self, uptime, results):
        ping, down, down_ratio, up, up_ratio, url = results
        worst_ratio = min(down_ratio, up_ratio)
        return config.telegram_message.format(
            provider=config.provider,
            down=down,
            up=up,
            ping=ping,
            ratio=worst_ratio * 100,
            uptime=uptime,
            reaction=self.get_reaction(down_ratio, up_ratio, ping),
            url=url,
        )

    def get_reaction(self, down_ratio, up_ratio, ping):
        if ping > config.movistar['ping'] \
                or down_ratio <= config.movistar['down_ratio'] \
                or up_ratio <= config.movistar['up_ratio']:
            return config.movistar['illegal']

        messages = [
            config.messages['terrible'],
            config.messages['bad'],
            config.messages['mediocre'],
            config.messages['fair'],
            config.messages['great'],
            config.messages['awesome'],
        ]
        max_idx = len(messages) - 1
        # convert the worst_ratio within the range [worst_legal - 1.0] to [0 - number_of_messages]
        worst_ratio = min(down_ratio, up_ratio)
        worst_legal = min(config.movistar['down_ratio'], config.movistar['up_ratio'])
        best_legal = 1.0
        coefficient = (0 - max_idx) / (worst_legal - best_legal)
        idx = coefficient * (worst_ratio - worst_legal)
        message_idx = min(int(math.ceil(idx)), max_idx)
        return messages[message_idx]


    def write(self, text, log=False):
        message = '%s - %s' % (self.timestamp(), text)
        print(message)
        if log:
            with open(config.base_path + '/error.log', 'a') as file:
                file.write('%s\n' % message)


    def timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    def insert_db(self, values):
        cn = mysql.connector.connect(host="127.0.0.1", database="homemonitor_db", user="pi", password="castellar", auth_plugin="mysql_native_password")
        sql_executer = cn.cursor()
        aql1 = "INSERT INTO isp (hour, latency, download, download_ratio, upload, upload_ratio) VALUES ("
        aql2 = ""
        for i in range (len(values)):
            values[i] = "\"" + str(values[i]) + "\""
            if (i!=5):
                values[i] += ","
            aql2 = aql2 + values[i]
        aql = aql1 + aql2 + ");"
        print (aql)
        sql_executer.execute(aql)
        cn.commit()


if __name__ == '__main__':
    isp = ISPMonitor()
    try:
        uptime = isp.get_uptime()
        isp.run_test()

        results = isp.parse_results()
        isp.send_warning(uptime, results)

        results.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        results.pop()
        isp.insert_db(results)

        isp.write('Finished')
    except Exception as e:
        isp.write(str(e), True)