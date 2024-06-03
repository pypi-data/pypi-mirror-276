# -*- coding: utf-8 -*-
"""
@Time : 2024/5/21 23:22 
@项目：studyPytest
@File : request_util.by
@PRODUCT_NAME :PyCharm
"""
import requests


class RequestUtil:
    session = requests.session()

    def send_request(self, method, url, data, **kwargs):
        method = method.lower()
        if method == 'get':
            return RequestUtil.session.request(method=method, url=url, params=data, **kwargs)
        elif method == 'post':
            return RequestUtil.session.request(method=method, url=url, json=data, **kwargs)
        elif method == 'put':
            return RequestUtil.session.request(method=method, url=url, params=data, **kwargs)
        elif method == 'delete':
            return RequestUtil.session.request(method=method, url=url, params=data, **kwargs)
        elif method == 'patch':
            return RequestUtil.session.request(method=method, url=url, params=data, **kwargs)
        else:
            raise Exception('不支持的请求方式')

    def send_request_file(self, method, file, url, data, **kwargs):
        file_data = {
            "file": open(file, 'rb')
        }
        return RequestUtil.session.request(method=method, url=url, files=file_data, json=data, **kwargs)
