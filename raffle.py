# -*- coding: utf-8 -*-
import requests
import yaml
import json
import time
from datetime import date
import logging
import logging.handlers

LOGIN_URL = 'http://17186.cn/n/login.jsp'
LOGIN_ACTION = 'http://17186.cn/ajax/account/staticLoginNew.action'
RAFFLE_INDEX = 'http://17186.cn/component/huodong/playflow/index.jsp'
RAFFLE_ACTION = 'http://17186.cn/ajax/lottery/shakePrize.action'
CHECK_ACTION = 'http://17186.cn/ajax/operation/userCheckIn.action'

GIF_INDEX_1 = 'http://17186.cn/component/huodong/playflow/gif.jsp?columnId=93533'
GIF_INDEX_2 = 'http://17186.cn/component/huodong/playflow/gif.jsp?columnId=93580'
GIF_ADD_LOG_ACTION = 'http://17186.cn/ajax/operation/addGifLog.action'
GIF_ADDCHANCE_ACTION = 'http://17186.cn/ajax/operation/addChance.action'

MEMBER_PAGE = 'http://17186.cn/component/member/index.jsp'
RED_ENVELOPE = 'http://17186.cn/ajax/member/memGR.action'

YAML_CONF = 'raffle.yaml'

LOG_FILE = 'raffle.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger('raffle')    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)


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
        login_params = {'userName': self.user, 'passWord': self.password}
        login_params['verifyCode'] = ''
        login_params['_'] = str(int(time.time()*1000))
        r = self.session.post(LOGIN_ACTION, data=login_params)
        resp_callback = r.text
        resp = json.loads(resp_callback)
        logger.info(resp)
        resp = json.loads(resp)
        if resp.get('resultCode') == 'ok':
            logger.info('login success')
            self.is_login = True
        else:
            logger.info('login failed')
            self.is_login = False

    def raffle(self):
        if self.is_login:
            r = self.session.get(RAFFLE_INDEX)
            r = self.session.post(RAFFLE_ACTION)
            resp = json.loads(r.text)
            logger.info(resp)
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

    def gif_add_chance(self):
        if self.is_login:
            # GIF 1
            r = self.session.get(GIF_INDEX_1)
            for i in range(4):
                r = self.session.post(GIF_ADD_LOG_ACTION, data={'id': '93533'})
            r = self.session.post(GIF_ADDCHANCE_ACTION, data={'type': '13', 'resource_code': '93533'})

            logger.info('gif view over 93533, add chance 2')

            # GIF 2
            r = self.session.get(GIF_INDEX_2)
            for i in range(4):
                r = self.session.post(GIF_ADD_LOG_ACTION, data={'id': '93580'})
            r = self.session.post(GIF_ADDCHANCE_ACTION, data={'type': '13', 'resource_code': '93580'})

            logger.info('gif view over 93580, add chance 2')

    def check(self):
        if self.is_login:
            r = self.session.post(CHECK_ACTION)
            logger.info(r.text)
        else:
            pass

    def red_envelope(self):
        today = date.today()
        if today.day == 8 or today.day == 18 or today.day == 28:
            r = self.session.get(MEMBER_PAGE)
            r = self.session.post(RED_ENVELOPE)

            logger.info('red envelop ' + r.text)




if __name__ == '__main__':
    http_bot = HttpRaffle()
    http_bot.login()
    time.sleep(3)
    http_bot.check()
    time.sleep(3)
    http_bot.gif_add_chance()
    time.sleep(3)
    http_bot.red_envelope()
    time.sleep(3)
    for i in range(13):
        time.sleep(5)
        http_bot.raffle()
