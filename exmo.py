import sys
import http.client
import urllib
import json
import hashlib
import hmac
import time
from datetime import datetime


class ExmoAPI:
    def __init__(self, API_KEY, API_SECRET, API_URL = 'api.exmo.me', API_VERSION = 'v1'):
        self.API_URL = API_URL
        self.API_VERSION = API_VERSION
        self.API_KEY = API_KEY
        self.API_SECRET = bytes(API_SECRET, encoding='utf-8')

    def sha512(self, data):
        H = hmac.new(key = self.API_SECRET, digestmod = hashlib.sha512)
        H.update(data.encode('utf-8'))
        return H.hexdigest()

    def api_query(self, api_method, params = {}):
        params['nonce'] = int(round(time.time() * 1000))
        params = urllib.parse.urlencode(params)

        sign = self.sha512(params)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Key": self.API_KEY,
            "Sign": sign
        }
        conn = http.client.HTTPSConnection(self.API_URL)
        conn.request("POST", "/" + self.API_VERSION + "/" + api_method, params, headers)
        response = conn.getresponse().read()

        conn.close()

        try:
            obj = json.loads(response.decode('utf-8'))
            if 'error' in obj and obj['error']:
                print(obj['error'])
                raise sys.exit()
            return obj
        except json.decoder.JSONDecodeError:
            print('Error while parsing response:', response)
            raise sys.exit()

def order_in_time(time_to_sleep, order_list):
    order_now(order_list)
    if len(order_list)>500:
        order_list = order_list[1:len(order_list)]
    print(order_list)
    time.sleep(time_to_sleep)
    order_in_time(time_to_sleep, order_list)

def order_now(order_list):
    ExmoAPI_instance = ExmoAPI('K-5224fd19278828fad24e3c12119885d92611eac5', 'S-50e52ffd0cd6d0a2416138105601d70236769d3b')
    ticker = (ExmoAPI_instance.api_query('ticker', {'pair': 'BTC_USD'}))
    t = str(datetime.now()).split('.')
    data = [t[0], (ticker.get('BTC_USD').get('buy_price')), (ticker.get('BTC_USD').get('sell_price'))]
    order_list = order_list.append(data)
    f = open('oders.txt', 'a')
    f.write(str(data))
    f.close()


order_list = []
delay = (60-int(str(datetime.now()).split('.')[0].split(' ')[1].split(':')[1]))
time.sleep((delay*60))
order_in_time(900, order_list)



