from urllib.parse import urlparse

import requests
import time
import re
import logging
import json
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

tianyi_session = requests.Session()


account_list = [{"user": "chinauncle", "pwd": "Aa159357", "uid": "malong"},
                {"user": "ChinaUncle89", "pwd": "HsjyuH7nnY6f8Wm", "uid": "malong"},
                {"user": "testjiji", "pwd": "rMtzMXjHPdU2m8w", "uid": "malong"},
                {"user": "18310428030", "pwd": "920918zyz", "uid": "ZhaoYaZai"}]
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
    # "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
    # "Host": "m.cloud.189.cn",
    "Accept-Encoding": "gzip, deflate",
}

domain = ''

# 获取主页地址


def getindexurl():
    #url = 'http://sh.china-noss-nrds.com/go_config/go?u=qq.football'
    url = 'https://www.ebay.com/usr/chinag'
    response = tianyi_session.get(url)
    pattern = re.compile('inline_value">[^/]+/([^/]+)')
    url = 'http://'+pattern.findall(response.text)[0].strip()
    get = tianyi_session.get(url)
    # str = u''
    # print(pattern.search(response.text))
    global domain
    domain = get.url
   # uri =pattern.findall(response.text)[0].strip() #urlparse(response.json()['url'])
   # domain = f'{uri.scheme}://{uri.netloc}'
    # domain = response.json()['url']


def checkin(account):
    rand = str(round(time.time() * 1000))
    url = f'{domain}/user/checkin?c={rand}'
    global headers
    result = tianyi_session.post(url=url, headers=headers, timeout=5).json()
    msgdic[account["uid"]] = msgdic.get(
        account["uid"], '')+account["user"]+result["msg"]+"\n"
    return result['msg']


def sendmsg(uid, msg):
    data = {"touser": uid, "msgtype": "text",
            "agentid": 1000002, "text": {"content": msg}}
    global access_token
    headers = {'content-type': "applicationjson;charset=UTF-8"}
    result = workweixin.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" +
                             access_token, data=json.dumps(data), headers=headers).json()
    print(result)


def login(account):
    rand = str(round(time.time() * 1000))
    url = f'{domain}/signin?c={rand}'
    data = {
        "email": account["user"],
        "passwd": account["pwd"],
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'Referer': domain,
    }
    r = tianyi_session.post(url, data=data, headers=headers, timeout=5)
    if r.json()['code'] == 200:
        return 'ok'
    else:
        return 'error'


access_token = ''
workweixin = requests.Session()
msgdic = {}


def main():
    getindexurl()
    global access_token
    access_token = workweixin.get(
        "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ww9b2cbed06bd0e2a2&corpsecret=-WML0IWaY-hq72K5oTJYSbbr0ROhwE_-7q0Fzr9iHCs").json()["access_token"]

    for account in account_list:

        logger.info("开始处理"+account["user"])
        msg = login(account)
        if msg != "error":
            logger.info(checkin(account))

    for key, value in msgdic.items():

        sendmsg(key, value)


def main_handler(event, context):
    main()


if __name__ == "__main__":
    main()
