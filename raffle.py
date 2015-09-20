# -*- coding: utf-8 -*-
import requests
import yaml
import json
import time

LOGIN_URL = 'http://17186.cn/n/login.jsp'
LOGIN_ACTION = 'http://17186.cn/ajax/account/staticLoginNew.action'
RAFFLE_ACTION = 'http://17186.cn/ajax/lottery/shakePrize.action'
CHECK_ACTION = 'http://17186.cn/ajax/operation/userCheckIn.action'
YAML_CONF = 'raffle.yaml'

class HttpRaffle:

    def __init__(self):
        config = yaml.load(open(YAML_CONF))
        login = config.get('main', {}).get('login', {})
        self.user = login.get('user', '')
        self.password = login.get('password', '')
        self.session = requests.Session()
        self.is_login = False

    def login(self):
        r = self.session.get(LOGIN_URL)
        jsoncallback = 'jQuery17105120323419105262_' + str(int(time.time()*1000))
        login_params = {'jsoncallback': jsoncallback, 'userName': self.user, 'passWord': self.password}
        login_params['verifyCode'] = ''
        login_params['_'] = str(int(time.time()*1000))
        r = self.session.post(LOGIN_ACTION, data=login_params)
        resp_callback = r.text
        resp = json.loads(resp_callback)
        resp = json.loads(resp)
        print resp
        if resp.get('resultCode') == 'ok':
            print 'login success'
            self.is_login = True
        else:
            print 'login failed'
            self.is_login = False

    def raffle(self):
        if self.is_login:
            r = self.session.post(RAFFLE_ACTION)
            resp = json.loads(r.text)
            print resp
            resp = json.loads(resp)
            code = resp.get('code')
            if code == '0000':
                pass
            elif code == '10001':
                pass
            elif code == '10002':
                pass
        else:
            pass

    def check(self):
        if self.is_login:
            r = self.session.post(CHECK_ACTION)
            print r.text
        else:
            pass


if __name__ == '__main__':
    http_bot = HttpRaffle()
    http_bot.login()
    http_bot.check()
    for i in range(9):
        http_bot.raffle()
