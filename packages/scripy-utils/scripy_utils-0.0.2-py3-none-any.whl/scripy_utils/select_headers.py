#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:skyoceanchen
# project_name:myself_exercise
# py_name :select_headers
# software: PyCharm
# datetime:2021/6/24 11:17
import json
import random

# 这个是PC + IE 的User-Agent
headers_pcUserAgent = {
    "safari 5.1 – MAC": "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "safari 5.1 – Windows": "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "IE 9.0": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
    "IE 8.0": "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "IE 7.0": "User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "IE 6.0": "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Firefox 4.0.1 – MAC": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Firefox 4.0.1 – Windows": "User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera 11.11 – MAC": "User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera 11.11 – Windows": "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Chrome 17.0 – MAC": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Maxthon": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Tencent TT": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "The World 2.x": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "The World 3.x": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "sogou 1.x": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "360": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Avant": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Green Browser": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
}
# 这个是Mobile + UC的User-Agent
headers_mobileUserAgent = {
    "iOS 4.33 – iPhone": "User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "iOS 4.33 – iPod Touch": "User-Agent:Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "iOS 4.33 – iPad": "User-Agent:Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Android N1": "User-Agent: Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Android QQ": "User-Agent: MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Android Opera ": "User-Agent: Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Android Pad Moto Xoom": "User-Agent: Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "BlackBerry": "User-Agent: Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "WebOS HP Touchpad": "User-Agent: Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Nokia N97": "User-Agent: Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Windows Phone Mango": "User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UC": "User-Agent: UCWEB7.0.2.37/28/999",
    "UC standard": "User-Agent: NOKIA5700/ UCWEB7.0.2.37/28/999",
    "UCOpenwave": "User-Agent: Openwave/ UCWEB7.0.2.37/28/999",
    "UC Opera": "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
}


def mobile_header(keys=None, urllib=False):
    mobile_keys_list = ['iOS 4.33 – iPhone', 'iOS 4.33 – iPod Touch', 'iOS 4.33 – iPad', 'Android N1', 'Android QQ',
                        'Android Opera ',
                        'Android Pad Moto Xoom', 'BlackBerry', 'WebOS HP Touchpad', 'Nokia N97', 'Windows Phone Mango',
                        'UC',
                        'UC standard', 'UCOpenwave', 'UC Opera']
    if not keys:
        keys = random.choice(mobile_keys_list)
    MUUA = headers_mobileUserAgent.get(keys)
    if urllib:
        return MUUA
    MUUA_split = MUUA.split(":")
    header = {}
    header[MUUA_split[0].strip()] = MUUA_split[1].strip()
    return header


def pc_header(keys=None, urllib=False):
    pc_list_list = ['safari 5.1 – MAC', 'safari 5.1 – Windows', 'IE 9.0', 'IE 8.0', 'IE 7.0', 'IE 6.0',
                    'Firefox 4.0.1 – MAC',
                    'Firefox 4.0.1 – Windows', 'Opera 11.11 – MAC', 'Opera 11.11 – Windows', 'Chrome 17.0 – MAC',
                    'Maxthon',
                    'Tencent TT', 'The World 2.x', 'The World 3.x', 'sogou 1.x', '360', 'Avant', 'Green Browser']
    if not keys:
        keys = random.choice(pc_list_list)
    PIUA = headers_pcUserAgent.get(keys)
    if urllib:
        return PIUA
    PIUA_split = PIUA.split(":")
    header = {}
    header[PIUA_split[0].strip()] = PIUA_split[1].strip()
    return header


UserAgents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

PROXIES = [
    '58.20.238.103:9797',
    '123.7.115.141:9797',
    '121.12.149.18:2226',
    '176.31.96.198:3128',
    '61.129.129.72:8080',
    '115.238.228.9:8080',
    '124.232.148.3:3128',
    '124.88.67.19:80',
    '60.251.63.159:8080',
    '118.180.15.152:8102'
]


# from fake_useragent import UserAgent
# ua = UserAgent()  # 实例化，实例化时需要联网但是网站不太稳定
# # print(ua.ie)  # 随机打印一个 ie 浏览器的头
# print(ua.random)  # 随机打印 User-Agent
# print("*3"*1000)


class User_Agent(object):
    """
        直接将 网页的源码复制下载之后, 可以使用此类进行解析
        self.user_agent_data 是 读取 文件的,
    """

    def __init__(self, json_file="fake_useragent_0.1.11.json"):
        """
        :param json_file: 下载后内容保存的文件
        """
        self.json_file = json_file
        self.ua_data = self.user_agent_data().get("browsers")
        self.b = ['chrome', 'opera', 'firefox', 'safari', 'internetexplorer']
        # -------
        self.chrome = lambda: random.choice(self.ua_data.get("chrome"))
        self.opera = lambda: random.choice(self.ua_data.get("opera"))
        self.firefox = lambda: random.choice(self.ua_data.get("firefox"))
        self.safari = lambda: random.choice(self.ua_data.get("safari"))
        self.ie = lambda: random.choice(self.ua_data.get("internetexplorer"))
        self.random = lambda: random.choice(self.ua_data.get(random.choice(self.b)))

    def user_agent_data(self):
        with open(self.json_file, "r") as fp:
            data = fp.read()
        return json.loads(data)


ua = User_Agent()
