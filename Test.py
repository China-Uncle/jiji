from urllib.parse import urlparse

import requests
import time

tianyi_session = requests.Session()

username = ""
password = ""

if username == "" or password == "":
    username = input("账号：")
    password = input("密码：")

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientId/355325117317828 clientModel/SM-G930K imsi/460071114317824 clientChannelId/qq proVersion/1.0.6',
    # "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
    # "Host": "m.cloud.189.cn",
    "Accept-Encoding": "gzip, deflate",
}

domain = ''


def main():
    getindexurl()
    msg = login(username, password)
    if msg != "error":
        checkin()


# 获取主页地址
def getindexurl():
    url = 'http://sh.china-noss-nrds.com/go_config/go?u=qq.football'
    response = tianyi_session.get(url)
    global domain
    uri = urlparse(response.json()['url'])
    domain = f'{uri.scheme}://{uri.netloc}'
    # domain = response.json()['url']


def checkin():
    rand = str(round(time.time() * 1000))
    url = f'{domain}/user/checkin?c={rand}'
    global headers
    result = tianyi_session.post(url=url, headers=headers, timeout=5)
    if result.json()['ret'] == 500:
        print(result.json()['msg'])
    else:
        print(result.json()['msg'])


def login(username, password):
    print(username)
    rand = str(round(time.time() * 1000))
    url = f'{domain}/signin?c={rand}'
    data = {
        "email": username,
        "passwd": password,
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


if __name__ == "__main__":
    main()
