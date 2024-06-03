# -*- coding: utf-8 -*-
"""
@Time : 2023/8/16 22:04 
@Author : skyoceanchen
@TEL: 18916403796
@项目：爬虫使用
@File : selenium_operation.by
@PRODUCT_NAME :PyCharm
"""
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException

# 规避检测
# option = webdriver.ChromeOptions()
# option.add_argument('--profile-directory=Default')
# option.add_argument("--disable-plugins-discovery");
# option.add_argument(
#     'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')# 设置请求头的User-Agent
# option.add_argument('--window-size=1280x1024') # 设置浏览器分辨率（窗口大小）
# option.add_argument('--start-maximized') # 最大化运行（全屏窗口）,不设置，取元素会报错
# option.add_argument('--disable-infobars') # 禁用浏览器正在被自动化程序控制的提示
# option.add_argument('--incognito') # 隐身模式（无痕模式）
# option.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
# option.add_argument('--disable-javascript') # 禁用javascript
# option.add_argument('--blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
# option.add_argument('--headless') # 浏览器不提供可视化页面  隐藏窗口
# option.add_argument('--ignore-certificate-errors') # 禁用扩展插件并实现窗口最大化
# option.add_argument('--disable-gpu') # 禁用GPU加速
# option.add_argument('–disable-software-rasterizer')
# option.add_argument('--disable-extensions')
# option.add_argument('--start-maximized')
# option.add_argument('--disable-javascript')  # 禁用javascript
# option.add_experimental_option('useAutomationExtension', False)
# option.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')

options = webdriver.ChromeOptions()
# options.add_argument('--headless') # 浏览器不提供可视化页面  隐藏窗口
options.add_argument('--disable-gpu')
# <editor-fold desc="关闭chrome密码登录时弹出的密码提示框">
prefs = {"": ""}
prefs["credentials_enable_service"] = False
prefs["profile.password_manager_enabled"] = False
options.add_experimental_option("prefs", prefs)
# </editor-fold>
# 防止打印一些无用的日志
options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
#  就是这一行告诉chrome去掉了webdriver痕迹 # 屏蔽webdriver特征
options.add_argument("--disable-blink-features=AutomationControlled")


# <editor-fold desc="控制浏览器滚动条缓慢下拉到最底">
def scroll_to_bottom(driver):
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0  # 当前窗口总高度
    new_height = driver.execute_script(js)
    while height < new_height:  # 将滚动条调整至页面底部
        for i in range(height, new_height, 100):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.1)
        height = new_height
        new_height = driver.execute_script(js)


# </editor-fold>
# <editor-fold desc="控制浏览器滚动条缓慢向上到顶">
def scroll_to_top(driver):
    js = "return action=document.body.scrollHeight"
    height = driver.execute_script(js)
    new_height = 0  # 当前窗口总高度
    js_top = "var q=document.documentElement.scrollTop={}"
    lis = list(range(new_height, height, 100))
    lis.reverse()
    for i in lis:
        driver.execute_script(js_top.format(i))
        time.sleep(0.1)


# </editor-fold>
# <editor-fold desc="滑动解锁">
def slide_to_unlock(driver):
    try:
        # #获取元素
        # //*[@id="nc_1_n1z"]
        nc_1_n1z = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        action = ActionChains(driver)
        # 鼠标左键按下不放
        action.click_and_hold(nc_1_n1z).perform()
        # 平行移动大于解锁的长度的距离
        #     拖动：
        # 1，drag_and_drop(soure=起始元素, target=结束元素)
        # 2，drag_and_drop_by_offset(soure=起始元素，xoffset，yoffset)，其中xoffset是水平便宜了，yoffset是垂直偏移量。
        action.drag_and_drop_by_offset(nc_1_n1z, 500, 0).perform()
    except UnexpectedAlertPresentException as e:
        print(e)


# </editor-fold>
driver = webdriver.Chrome(options=options)  # 这里是写chrome的地址
