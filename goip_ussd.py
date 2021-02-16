import requests
import re
import time
import subprocess
import xml.etree.ElementTree as ET

class Goip_ussd:
    def __init__(self, goip_url, goip_login = "admin", goip_passw= "admin", goip_ussd="*100#",lines_count=8,goip_ussd_line={}):
        self.smskey=None
        self.lines_count=lines_count
        self.time_sleep = 10
        self.goip_url = goip_url
        self.goip_login = goip_login
        self.goip_passw = goip_passw
        self.goip_ussd =goip_ussd
        self.goip_ussd_line = goip_ussd_line

    def get_smskey(self):
        url_smskey = self.goip_url+'/default/en_US/ussd_info.html?type=ussd'
        resp = requests.get(url_smskey,auth=(self.goip_login, self.goip_passw))

        if resp.status_code == 200:
            regex = r"\"([0-9a-fA-F]{8})\""
            m = re.findall(regex, resp.text, re.IGNORECASE)
            try:
                self.smskey = m[0]
            except NameError:
                self.smskey = None    
    
    def send_ussd(self):
        if self.smskey != None:
            url_ussd = self.goip_url+'/default/en_US/ussd_info.html'
            data = {"type": "ussd", "smskey": self.smskey, "action":"USSD", "telnum":self.goip_ussd, "send":"Send"}
            line = 1
            while line <= self.lines_count: 
                data.update({"line"+str(line):"1"})
                line+=1
            resp = requests.post(url_ussd,auth=(self.goip_login, self.goip_passw),data=data)
            return resp
        else:
            return None

    def get_response(self):
        balance_return = {}
        usr_sms_status = self.goip_url+'/default/en_US/send_sms_status.xml?line=&ajaxcachebust='+str(int(time.time())) 
        resp = None
        time.sleep(self.time_sleep)
        resp = requests.get(usr_sms_status,auth=(self.goip_login, self.goip_passw))
        root = ET.fromstring(resp.content) 
        line = 1
        while line <= self.lines_count: 
            balance_return.update({line: root.find('error'+str(line)).text})
            line+=1
        return balance_return

    def close_ussd(self):
        url_ussd = self.goip_url+'/default/en_US/ussd_info.html'
        data = {"type": "ussd", "smskey": self.smskey, "action":"USET", "telnum":"", "send":"Disconnect"}
        line = 1
        while line <= self.lines_count: 
            data.update({"line"+str(line):"1"})
            line+=1
        requests.post(url_ussd,auth=(self.goip_login, self.goip_passw),data=data)
