import os
import json
import time
import random
import requests
from lxml import html

class util:
    def getCC(self,country):
        filepath = os.path.join(os.path.dirname(__file__),'countryCode.json')
        with open(filepath) as jsonFile:
            data = json.load(jsonFile)
        return data[country]

class generator:
    def __init__(self,):
        self.url = 'https://smsreceivefree.com/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.logger = print # default logger is stdout
    
    def setLogger(self, log):
        self.logger = log

    def resetVars(self):
        self.country = None
        self.number = None
        self.path = None
        self.numbers = None
        self.paths = None

    def getAvailableNumbers(self,country):
        self.logger("Setting SMS country to {}".format(country))
        self.country = country
        url = "{0}country/{1}".format(self.url, country)
        r = requests.get(url, headers=self.headers)
        tree = html.fromstring(r.content)
        self.logger("Populating numbers list...")
        self.numbers = tree.xpath('//*[@class="row"]/a/text()')
        self.logger("Populating paths list...")
        self.paths = tree.xpath('//*[@class="row"]/a/@href')
        return numbers

    def selectNumber(self,number):
        self.logger("Attemping to select number: {}".format(number))
        # if vars aren't set, we probably expired
        if self.country == None or self.numbers == None:
            self.logger("Cannot select number--class variables are empty")
            return False
        # refresh number list
        self.getAvailableNumbers(self.country)
        # find the corresponding number
        for i,num in enumerate(self.numbers):
            if number in num:
                self.number = num.split(" ")[0]
                self.path = self.paths[i]
                self.logger("Selected number: {} (path: {})".format(self.number, self.path))
                return True
        self.logger("Number ({}) not found in list--variables might have \
                expired. Clearing class variables...".format(number))
        self.resetVars()
        return False

    def checkSMS(self,pattern):
        if self.number == None or self.path == None:
            self.logger("Unable to check {} for messages. Number/path is empty".format(self.number))
            return (False,[])
        self.logger("Checking {} for new messages...".format(self.number))
        url = "{0}{1}/".format(self.url,self.path)
        r = requests.get(url, headers=self.headers)
        tree = html.fromstring(r.content)
        sender = tree.xpath('//*[@class="messagesTable"]/tbody/tr/td[1]/text()')
        message = tree.xpath('//*[@class="messagesTable"]/tbody/tr/td[3]/text()')
        print(message)
        print(type(message))
        '''
        for x in range(5):
            if pattern in message[x]:
                return message[x]
                break
        '''