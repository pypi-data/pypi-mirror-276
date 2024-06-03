"""
@Time : 2023/5/25 11:25 
@Author : skyoceanchen
@TEL: 18916403796
@项目：WaterSystemCarMounted
@File : url_parse_operations.by
@PRODUCT_NAME :PyCharm
"""
from urllib import parse

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
