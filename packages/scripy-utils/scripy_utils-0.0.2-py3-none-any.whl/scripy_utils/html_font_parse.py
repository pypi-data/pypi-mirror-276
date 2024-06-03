"""
@Time : 2023/5/25 11:26 
@Author : skyoceanchen
@TEL: 18916403796
@项目：WaterSystemCarMounted
@File : font_parse.by
@PRODUCT_NAME :PyCharm
"""
from fontTools.ttLib import TTFont
from io import BytesIO
import requests
import time
import re
import chardet


# 解析文章的特殊字体
class HtmlParserFont(object):
    """
    lis = ['https://qidian.gtimg.com/qd_anti_spider/ffizRldi.ttf ', 'https://qidian.gtimg.com/qd_anti_spider/LcvsjEcp.ttf']
    print(get_font(lis[1]))
    """

    # <editor-fold desc="获取文章的特殊字体">
    def get_html_info_fint(self, htmlContent):
        # 获取网页的文字ttf文件的地址
        url_ttf_pattern = re.compile('<style>(.*?)\s*</style>', re.S)
        fonturl = re.findall(url_ttf_pattern, htmlContent)[0]
        url_ttf = re.search('woff.*?url.*?\'(.+?)\'.*?truetype', fonturl).group(1)
        # 获取所有反爬的数字
        word_pattern = re.compile('</style><span.*?>(.*?)</span>', re.S)  # 制定正则匹配规则，匹配所有<span>标签中的内容
        numberlist = re.findall(word_pattern, htmlContent)
        return url_ttf, numberlist

    # </editor-fold>
    def get_font(self, url):
        """
        获取源代码中数字信息与英文单词之间的映射关系
        :param url: <str> 网页源代码中的字体地址
        :return: <dict> 网页字体映射关系
        """
        time.sleep(1)
        response = requests.get(url)
        font = TTFont(BytesIO(response.content))
        web_font_relation = font.getBestCmap()
        font.close()
        return web_font_relation


class ChardetParse(object):
    # 如果安装了Anaconda，chardet就已经可用了。否则，需要在命令行下通过pip安装：
    # $ pip install chardet
    # 如果遇到Permission denied安装失败，请加上sudo重试。
    # 使用chardet
    # 当我们拿到一个bytes时，就可以对其检测编码。用chardet检测编码，只需要一行代码：
    # print(chardet.detect(b'Hello, world!'))  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
    # data = '离离原上草，一岁一枯荣'.encode('gbk')
    # print(chardet.detect(data))  # {'encoding': 'GB2312', 'confidence': 0.7407407407407407, 'language': 'Chinese'}
    data = '最新の主要ニュース'.encode('euc-jp')

    # print(chardet.detect(data),
    #       type(chardet.detect(data)))  # {'encoding': 'EUC-JP', 'confidence': 0.99, 'language': 'Japanese'}
    def encoding_code_type(self, msg):
        return chardet.detect(msg).get("encoding")
