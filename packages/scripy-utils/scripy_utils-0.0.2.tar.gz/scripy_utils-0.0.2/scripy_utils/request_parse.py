"""
@Time : 2023/5/25 11:32 
@Author : skyoceanchen
@TEL: 18916403796
@项目：WaterSystemCarMounted
@File : request_parse.by
@PRODUCT_NAME :PyCharm
"""
import json
import random
from urllib import parse

'''
headers = """accept: application/json, text/plain, */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8
cache-control: no-cache
cookie: _ga=GA1.2.221399358.1578065734; __gads=ID=4df8a0420d9d97d4:T=1578065745:S=ALNI_MZLl3VF82H__z73FimSvjSPEEP3bw; UM_distinctid=170cf17a7bb413-0ddca1483240a5-4313f6b-144000-170cf17a7bd5f5; Hm_lvt_f1efa4dd0c4c1bdecd84dd62ecd602bc=1584714581; sc_is_visitor_unique=rx10890287.1585142350.D77706BECC854FF6BCE903A6B0BBAF9B.2.2.2.2.2.2.2.2.2; .CNBlogsCookie=BB254006969E71F3A98F5083C38181D35004ACCECDE4613542084BFA090A3887F4A94C45F72CBF961EEFCCFC091C030DACCF90BED81EB1A536F43977A83391E29CF9A8A0B47A4426A252897783333BBC75FEA283; _gid=GA1.2.1238470412.1587021206; .Cnblogs.AspNetCore.Cookies=CfDJ8B9DwO68dQFBg9xIizKsC6S-uJdcDdi_D3jcrVPifdxLT_LnW-CRpQc4LTd5Eph4WFGp8PxkTjH9DSYOT2H1iThP-KSsHl8IEaenQ8Gjb_6VBHAxSRe2-qdsyT9KC5Nf9PbK1ayiNBdpMeQSq0-ryK4MTQqukbztxIPZa6LHFRunAemQJpCtZWf-Gws2jHqi0vlt4lvdjSoFDpXFgwEu9Wj57la3c_fc4LvM23-XcRd6_37tg-O6FTuKproEmlRKo8IwH3dINLpgF6T5FOSq5qr6lT04uqawrOW81AZ2pJ8QSSquV9BuHXaQaWx6q_6OArQEOhEYF2dtZ7UtFIKyTQ92wtGWmkDULy87iHX1W7MV71e6PrtS3zDpdNHglEegeQtgh_oa-9eDZEUk2XfDlrvchPhUDNM_2DshOithXXgIxlAnzPMRmeSlEv0ClCTeN_kCKfmjINNB4SpEWBlISk1AoJCGyqRG4-2WphYtuWlh06MIpuSErFWYja39McH5-8m6UULAhiK2jYFe_-IFBm_S_-1yogWHue9A5jIG6Th_YUWZYyEybRW5DyAFPMcOnQ; _gat_gtag_UA_48445196_1=1
pragma: no-cache
referer: https://i-beta.cnblogs.com/posts/edit
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 chrome-extension chrome-extension
x-blog-id: 526720
"""

'''


class RequestParse(object):
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
        "Green Browser": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
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

    # <editor-fold desc="分析header">
    def analysis_header(self, headers):
        header_list = headers.strip(' ').strip('\n').split('\n')
        # print(header_list)
        header_lis = dict()
        for header in header_list:
            # pass
            # print(header_list)
            # header = head.split(':')
            header_lis[header.split(":", 1)[0]] = header.split(":", 1)[1]
        return header_lis

    # </editor-fold>

    # <editor-fold desc="分析cookies">
    def analysis_cookies(self, cookies):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }
        url = 'https://www.yaozh.com/member/'
        # cookies是一个字典或者对象
        # cookies = "acw_tc=2f624a6c15681000021367682e6b3e0142e0d99eb63cf4b240f962532ebfef; PHPSESSID=09f00am6llg7cmodj751rj8b54; _ga=GA1.2.1617503464.1568100004; _gid=GA1.2.1446416891.1568100004; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1568100005; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1568100020"
        # cookies = "hello=1; _ga=GA1.2.1304839036.1579713995; _gid=GA1.2.300468293.1580308967; rr=https://cn.aq101.club/; last_login=ceshi%40qq.com; lt=eyJpdiI6IkNMcXFVeFplOVorV2xydnVwcDRqVGc9PSIsInZhbHVlIjoicXlpREIyQ2FFUHFGWitKN1NLNlZRWFhHRXNKOXBsbEV6RUdFc09Jait0cz0iLCJtYWMiOiJiOTVkMzUzMGZiOWZjOTRlMWNmYjY5ODFjODRiMmYwYWI2NGRmNWQxNmJmNmNkMGNjYjMwZjQzZjViNjliNTY4In0%3D; _gat_gtag_UA_78207029_9=1; XSRF-TOKEN=eyJpdiI6IlM2T2hkWjZcL0F3d0VCMEN3a2pOb0h3PT0iLCJ2YWx1ZSI6ImN4eDZaU2RseUQ2OVhySFhpYUUwZHBxc0IxaXVTQ1JSc2pFTWx3Q1BQbExjSUJBNUlPNHdGYllva1RBZzIxc2QiLCJtYWMiOiI5ZGZiODJkMDgzYzA3YmVhMmFkZWUyNjNhMDgzMWM0NjUzNTRjYWVjODM2ZjIyNTY2ZmRkOTJhYzRmMTEzN2U3In0%3D; miao_cn=eyJpdiI6Im1pZzBFZEl6UzFzd01HMGV3c2lab1E9PSIsInZhbHVlIjoiNzNmQmZlOG5UdXcxa0JjMmVIWldRZUg5cXRcL1BTRnZPXC9uZk8wM044WlhnWlFONGEzdlRUU1F2NnJyOGZBbTFSIiwibWFjIjoiN2QwNDBmZjI2YzZkNDI0YzE0MGZhNGY3NWRiZmFlMWU0NjMxNjhjMmVhY2Y2ZTVhYmM5MzdlZjA5NjYzMDFlZCJ9"
        # cookies = "lianjia_uuid=53fb8ed4-d6dd-4223-bf03-9a95c5a3abb5; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216fd6645af54be-0b5f0714a2a0e1-7711439-1327104-16fd6645af7376%22%2C%22%24device_id%22%3A%2216fd6645af54be-0b5f0714a2a0e1-7711439-1327104-16fd6645af7376%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; crosSdkDT2019DeviceId=-shytl0-84as1-33we6te3dky6iv5-203i1t2pz; login_ucid=2000000096534040; lianjia_token=2.0057730a462b2899b246de2377d6542c94; lianjia_ssid=8e0ae7f4-c548-4e19-9dae-4d2a6d6fcb16; select_city=310000"
        # cookies = '_ga=GA1.2.221399358.1578065734; __gads=ID=4df8a0420d9d97d4:T=1578065745:S=ALNI_MZLl3VF82H__z73FimSvjSPEEP3bw; UM_distinctid=170cf17a7bb413-0ddca1483240a5-4313f6b-144000-170cf17a7bd5f5; Hm_lvt_f1efa4dd0c4c1bdecd84dd62ecd602bc=1584714581; sc_is_visitor_unique=rx10890287.1585142350.D77706BECC854FF6BCE903A6B0BBAF9B.2.2.2.2.2.2.2.2.2; .CNBlogsCookie=BB254006969E71F3A98F5083C38181D35004ACCECDE4613542084BFA090A3887F4A94C45F72CBF961EEFCCFC091C030DACCF90BED81EB1A536F43977A83391E29CF9A8A0B47A4426A252897783333BBC75FEA283; _gid=GA1.2.1238470412.1587021206; .Cnblogs.AspNetCore.Cookies=CfDJ8B9DwO68dQFBg9xIizKsC6S-uJdcDdi_D3jcrVPifdxLT_LnW-CRpQc4LTd5Eph4WFGp8PxkTjH9DSYOT2H1iThP-KSsHl8IEaenQ8Gjb_6VBHAxSRe2-qdsyT9KC5Nf9PbK1ayiNBdpMeQSq0-ryK4MTQqukbztxIPZa6LHFRunAemQJpCtZWf-Gws2jHqi0vlt4lvdjSoFDpXFgwEu9Wj57la3c_fc4LvM23-XcRd6_37tg-O6FTuKproEmlRKo8IwH3dINLpgF6T5FOSq5qr6lT04uqawrOW81AZ2pJ8QSSquV9BuHXaQaWx6q_6OArQEOhEYF2dtZ7UtFIKyTQ92wtGWmkDULy87iHX1W7MV71e6PrtS3zDpdNHglEegeQtgh_oa-9eDZEUk2XfDlrvchPhUDNM_2DshOithXXgIxlAnzPMRmeSlEv0ClCTeN_kCKfmjINNB4SpEWBlISk1AoJCGyqRG4-2WphYtuWlh06MIpuSErFWYja39McH5-8m6UULAhiK2jYFe_-IFBm_S_-1yogWHue9A5jIG6Th_YUWZYyEybRW5DyAFPMcOnQ; _gat_gtag_UA_48445196_1=1'
        cook_dic = dict()
        cookies_list = cookies.split('; ')
        for cook in cookies_list:
            cook_dic[cook.split('=')[0]] = cook.split('=')[1]
        # reponse = requests.get(url=url,headers = headers,cookies = cook_dic)
        # print(reponse.content.decode())
        print(cook_dic)

    # </editor-fold>

    # <editor-fold desc="手机header -useragent">
    def mobile_header(self, keys=None, urllib=False):
        mobile_keys_list = ['iOS 4.33 – iPhone', 'iOS 4.33 – iPod Touch', 'iOS 4.33 – iPad', 'Android N1', 'Android QQ',
                            'Android Opera ',
                            'Android Pad Moto Xoom', 'BlackBerry', 'WebOS HP Touchpad', 'Nokia N97',
                            'Windows Phone Mango',
                            'UC',
                            'UC standard', 'UCOpenwave', 'UC Opera']
        if not keys:
            keys = random.choice(mobile_keys_list)
        MUUA = RequestParse.headers_mobileUserAgent.get(keys)
        if urllib:
            return MUUA
        MUUA_split = MUUA.split(":")
        header = {}
        header[MUUA_split[0].strip()] = MUUA_split[1].strip()
        return header

    # </editor-fold>
    def pc_header(self, keys=None, urllib=False):
        pc_list_list = ['safari 5.1 – MAC', 'safari 5.1 – Windows', 'IE 9.0', 'IE 8.0', 'IE 7.0', 'IE 6.0',
                        'Firefox 4.0.1 – MAC',
                        'Firefox 4.0.1 – Windows', 'Opera 11.11 – MAC', 'Opera 11.11 – Windows', 'Chrome 17.0 – MAC',
                        'Maxthon',
                        'Tencent TT', 'The World 2.x', 'The World 3.x', 'sogou 1.x', '360', 'Avant', 'Green Browser']
        if not keys:
            keys = random.choice(pc_list_list)
        PIUA = RequestParse.headers_pcUserAgent.get(keys)
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


"""
HTTP请求头中的一些字符有特殊含义，转义的时候不会保留，如下：
加号（+）会转换成空格
正斜杠（/）分隔目录和子目录
问号（?）分隔URL和查询参数
百分号（%）制定特殊字符
#号指定书签
&号分隔参数

如若要在HTTP请求头中保留这些特殊字符，需将其转换成百分号（%）加对应的十六进制ASCII码，如：
+ ： %2B
空格 ： %20
/ ： %2F
? ： %3F
% ： %25
# ： %23
& ： %26
= ： %3D

 // URL内中文编码
 String s2 = Utils.encodeURIComponent(stringURL, "UTF-8");
 // ：和/都会被编码，导致http链接就会失效处理
 sEncodeURL = s2.replaceAll("\\%3A", ":").replaceAll("\\%2F", "/");
"""


class UrlParse(object):
    # 字典转换成url参数
    def dict_to_url_params(self, params: dict):
        """
        dic = {'username': 'username', 'password': 'password',}
        :param dic:
        :return: username=username&password=password
        """
        return parse.urlencode(params)

    # url参数转换成字典
    def url_params_to_dic(self, params: str):
        """
        params = 'https://www.baidu.com/s?&wd=python&ie=utf-8'或者
        params = '&wd=python&ie=utf-8'
        :param params:
        :return:{'wd': 'python', 'ie': 'utf-8'}
        """
        url = 'https://www.baidu.com/s?&wd=python&ie=utf-8'
        # 提取url参数
        if '?' in params:
            query = parse.urlparse(params).query  # wd=python&ie=utf-8
        else:
            query = params
        # 将字符串转换为字典
        params = parse.parse_qs(query)  # {'wd': ['python'], 'ie': ['utf-8']}
        """所得的字典的value都是以列表的形式存在，若列表中都只有一个值"""
        result = {key: params[key][0] for key in params}
        return result

    # 汉字转换成unicode编码
    def chinese_to_unicode(self, params: str, special_characters=False):
        """
        URL只允许一部分ASCII字符，其他字符（如汉字）是不符合标准的，此时就要进行编码。
        :param params:A中B国
        :return:A%E4%B8%ADB%E5%9B%BD
        :param special_characters:
        quote_plus 编码了斜杠,加号等特殊字符
        """
        if special_characters:
            return parse.quote_plus(params)
        else:
            return parse.quote(params)

    # unicode编码转换成汉字
    def unicode_to_chinese(self, params: str, special_characters=False):
        """
        :param params:A%E4%B8%ADB%E5%9B%BD
        :param special_characters:
        :return:A中B国
        unquote_plus 把加号解码成空格等特殊字符
        """
        if special_characters:
            return parse.unquote_plus(params)
        else:
            return parse.unquote(params)

    def django_url(self, url):
        yuan = "sian/data/传感器平剖面图/沉降计/平面/S2-DD1.jpg"
        path3 = "sian/data/%E4%BC%A0%E6%84%9F%E5%99%A8%E5%B9%B3%E5%89%96%E9%9D%A2%E5%9B%BE/%E6%B2%89%E9%99%8D%E8%AE%A1/%E5%B9%B3%E9%9D%A2/S2-DD1.jpg"
        path2 = "sian/data/%25B4%25AB%25B8%25D0%25C6%25F7%C6%BD%25C6%25CA%25C3%25E6%CD%BC/%25B3%25C1%25BD%25B5%25BC%25C6/%C6%BD%25C3%25E6/S2-DD1.jpg"
        path1 = "sian/data/%B4%AB%B8%D0%C6%F7ƽ%C6%CA%C3%E6ͼ/%B3%C1%BD%B5%BC%C6/ƽ%C3%E6/S2-DD1.jpg"
        # web_url = parse.quote(yuan)
        # print(urlencode({"a": "传感器平剖面图"}))
        # print(1, web_url.encode('gb2312'))
        # print(2, urlparse(web_url))
        # print("path1", parse.quote(web_url)  # .replace('2525','25')
        #       )

        # 按照gn2312格式进行2次urlencode编码
        gn2312_encoded = parse.quote(parse.quote(yuan, encoding='gb2312'))
        # 按照utf8格式进行1次urlencode编码
        utf8_encoded = parse.quote(yuan)
        print("gn2312编码结果：", gn2312_encoded)
        print("utf8编码结果：", utf8_encoded)
        print("utf8编码结果：", parse.unquote(utf8_encoded))
        print("utf8编码结果path1：", parse.unquote(path1.encode('utf-8'), encoding='gb2312'))
        print("utf8编码结果path2：", parse.unquote(parse.unquote(path2, encoding='gb2312'), encoding='gb2312'))


if __name__ == '__main__':
    dic = {"data": {"producer": "SRS", "server_address": "47.103.195.119:9876", "domain": "", "topic": "XIY-SRS-GJ",
                    "tags": "ALL", "message_key": "", "access_secret": "", "access_key": "", "channel": "",
                    "send_body": "{\"producer\": \"SRS\", \"from\": \"MQ-SRS-001\", \"bizId\": \"XIY-SRS-GJ-20231205162613-accc41b4\", \"time\": \"2023-12-05 16:26:13\", \"data\": [{\"createTime\": \"2023-06-16 15:01:05\", \"alarmTd\": 5, \"runwayCode\": \"S1\", \"alarmType\": \"\\u573a\\u9053\\u5de1\\u68c0\\u544a\\u8b66\", \"reason\": \"\\u677f\\u5757\\u7834\\u788e\", \"postion\": \"s1 \\u8dd1\\u9053\\uff0c**\\u533a\\u57df\\uff0c**\\u5355\\u5143\\uff0c5 \\u884c4 \\u5217\", \"x\": 12345678.0, \"y\": 12345678.0, \"handle\": 1, \"level\": 1, \"eventDescription\": \"\\u5de1\\u68c0\\u533a\\u57df\\u65ad\\u677f\\u6570\\u91cf\\u8d85\\u8fc7\\u677f\\u5757\\u6570\\u91cf10%\", \"measure\": [\"\\u5efa\\u8bae\\u5f00\\u5c55\\u9053\\u9762\\u7ed3\\u6784\\u4e13\\u9879\\u6d4b\\u8bd5\\u8bc4\\u4f30\\uff0c\\u660e\\u786e\\u9053\\u9762\\u65ad\\u677f\\u53d1\\u5c55\\u6210\\u56e0\\uff0c\\u5236\\u5b9a\\u6280\\u672f\\u63aa\\u65bd\\u4fee\\u590d\\u65e2\\u6709\\u75c5\\u5bb3\\u5e76\\u5ef6\\u7f13\\u5176\\u53d1\\u5c55\", \"\\u5efa\\u8bae\\u5f00\\u5c55\\u9053\\u9762\\u7ed3\\u6784\\u4e13\\u9879\\u6d4b\\u8bd5\\u8bc4\\u4f30\\uff0c\\u660e\\u786e\\u9053\\u9762\\u65ad\\u677f\\u53d1\\u5c55\\u6210\\u56e0\\uff0c\\u5236\\u5b9a\\u6280\\u672f\\u63aa\\u65bd\\u4fee\\u590d\\u65e2\\u6709\\u75c5\\u5bb3\\u5e76\\u5ef6\\u7f13\\u5176\\u53d1\\u5c55\", \"\\u5efa\\u8bae\\u5f00\\u5c55\\u9053\\u9762\\u7ed3\\u6784\\u4e13\\u9879\\u6d4b\\u8bd5\\u8bc4\\u4f30\\uff0c\\u660e\\u786e\\u9053\\u9762\\u65ad\\u677f\\u53d1\\u5c55\\u6210\\u56e0\\uff0c\\u5236\\u5b9a\\u6280\\u672f\\u63aa\\u65bd\\u4fee\\u590d\\u65e2\\u6709\\u75c5\\u5bb3\\u5e76\\u5ef6\\u7f13\\u5176\\u53d1\\u5c55\"]}]}"}
           }
    print(UrlParse().dict_to_url_params(dic))
