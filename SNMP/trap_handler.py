#!/usr/bin/env python
import os
import sys
import json
import requests
import pprint

class TrapHandler():
    def __init__(self):
        self.read_keys()

    def read_trap(self):
        with open("/var/log/traps.log") as myFile:
            text = myFile.read()
            myFile.close()
            result = text.split('/////')
            self.format_message(result)

    def insert_split_character(self):
        with open("/var/log/traps.log", 'a+') as myFile:
            myFile.write('/////')
            myFile.close()
        self.read_trap()

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

    def format_message(self,result):
        line1 = result[-4].split(' ')
        message =  "Received new trap message: \n"
        message +=  "--------------------------------------\n"
        message += "Date: " + line1[0] + '  ' + line1[1] + "\n"
        message += "HostName: " + line1[2] + "\n\n"
        message += "Trap Info: \n" + str(result[-4])
        self.send_warning(message)


if __name__ == '__main__':
    handler = TrapHandler()
    handler.insert_split_character()