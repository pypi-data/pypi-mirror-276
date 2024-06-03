# -*- coding: utf-8 -*-
"""
@Time : 2024/5/27 11:18 
@项目：api_test
@File : seleuim_util.by
@PRODUCT_NAME :PyCharm
"""

import random
import re
import time
import urllib.request

import cv2
from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
"""
options = webdriver.ChromeOptions()
# option.add_argument(('--proxy-server=' + ip))  # 有的博客写的是'--proxy-server=http://'，就目前我的电脑来看的话需要把http://去掉就可以用，他会自己加的
# options.add_argument('--disable-gpu')# 禁用GPU加速
options.add_argument('--disable-javascript')  # 禁用javascript
options.add_argument('--incognito')  # 隐身模式（无痕模式）
options.add_argument('--profile-directory=Default')
options.add_argument("--disable-plugins-discovery")
options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')  # 设置请求头的User-Agent
options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
# options.add_argument('--headless')  # 浏览器不提供可视化页面  隐藏窗口
options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
options.add_argument('–disable-software-rasterizer')
options.add_argument('--disable-extensions')
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')
# <editor-fold desc="关闭chrome密码登录时弹出的密码提示框">
prefs = {"": ""}
prefs["credentials_enable_service"] = False
prefs["profile.password_manager_enabled"] = False
options.add_experimental_option("prefs", prefs)
# </editor-fold>
# 防止打印一些无用的日志

options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
这个选项用于从Chrome启动命令行开关中排除特定的参数。在这种情况下，它排除了--enable-automation开关。--enable-automation通常用于标识浏览器是在自动化控制下运行，比如在Selenium测试中。排除这个开关可能有助于在某种程度上隐藏自动化脚本的行为，使得浏览器看起来更像由人类操作，从而可能有助于绕过一些网站的反爬虫策略。

#  就是这一行告诉chrome去掉了webdriver痕迹 # 屏蔽webdriver特征
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)  # 这里是写chrome的地址



detach 参数：
option.add_experimental_option("detach", True)
这个选项使得Chrome浏览器进程在Selenium控制台窗口关闭后仍然保持打开状态。默认情况下，当你关闭Selenium控制台或结束会话时，与之关联的浏览器窗口也会关闭。当detach设置为True时，浏览器窗口会在后台继续运行，即使Selenium WebDriver不再与它交互。这在进行长时间运行的任务或者需要浏览器在脚本执行完成后仍然保持打开状态时非常有用。
结合这两个选项，你可以在自动化测试中让Chrome浏览器以一种更隐蔽的方式运行，并且在测试完成后浏览器窗口不会立即关闭。
"""
from selenium.webdriver import ActionChains


#  浏览器
class SeleniumChromeUtil():
    def __init__(self, add_argument=None, psd_alert=True, service=None, browser="Edge"):
        # add_argument = ('--start-maximized',)
        self.get_options(browser, psd_alert, add_argument)
        if browser == "Chrome":
            self.driver = webdriver.Chrome(
                options=self.options,
                service=webdriver.chrome.service.Service(service)
            )  # 调用谷歌内核
        elif browser == "Edge":
            self.driver = webdriver.Edge(
                options=self.options,
                service=webdriver.edge.service.Service(service)
            )  # 调ege内核

    def get_options(self, browser, psd_alert, add_argument):
        if browser == "Chrome":
            self.options = webdriver.ChromeOptions()
        elif browser == "Edge":
            self.options = webdriver.EdgeOptions()
        if psd_alert:
            self.close_psd_alert()
        if add_argument:
            self.add_argument(add_argument)

    # <editor-fold desc="解决特征识别">
    def feature_recognition(self):
        """
        如果不采取去除特征识别，即以下两行代码。则页面的滑块验证码在滑动后，会显示如下图的出错，从而阻止登录进行。
        因为服务器识别到的selenium的特征。使用该两行代码更改了特征，即可以顺利通过识别。
        :return:
        """
        script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
        self.driver.execute_script(script)

    # </editor-fold>
    # <editor-fold desc="模拟登陆时就被检测,进行绕过检测">
    def bypass_detection(self):
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                      Object.defineProperty(navigator,'webdriver',{
                        get: () => undefined
                      })
                      """
        })

    # </editor-fold>

    def driver_url(self, url):
        self.driver.get(url, )

    # 弹出框
    # <editor-fold desc="关闭chrome密码登录时弹出的密码提示框">
    def close_psd_alert(self):
        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        self.options.add_experimental_option("prefs", prefs)

    # </editor-fold>
    def add_argument(self, args: list):
        for arg in args:
            if isinstance(arg, str):
                self.options.add_argument(arg)
            else:
                for k, v in arg.items():
                    self.options.add_experimental_option(k, v)

    # <editor-fold desc="控制浏览器滚动条缓慢下拉到最底">
    def scroll_to_bottom(self, wait_time=1, every_height=100):
        js = "return action=document.body.scrollHeight"
        # 初始化现在滚动条所在高度为0
        height = 0  # 当前窗口总高度
        new_height = self.driver.execute_script(js)
        while height < new_height:  # 将滚动条调整至页面底部
            for i in range(height, new_height, every_height):
                self.driver.execute_script('window.scrollTo(0, {})'.format(i))
                time.sleep(wait_time)
            height = new_height
            new_height = self.driver.execute_script(js)

    # </editor-fold>
    # <editor-fold desc="控制浏览器滚动条缓慢向上到顶">
    def scroll_to_top(self, new_height=0, wait_time=0.1, every_height=100):
        """
        :param new_height:当前窗口总高度
        :param wait_time:每次调用时间
        :param every_height:每次页面跳动的高度
        :return:
        """
        js = "return action=document.body.scrollHeight"
        height = self.driver.execute_script(js)
        new_height = new_height  # 当前窗口总高度
        js_top = "var q=document.documentElement.scrollTop={}"
        lis = list(range(new_height, height, every_height))
        lis.reverse()
        for i in lis:
            self.driver.execute_script(js_top.format(i))
            time.sleep(wait_time)

    # </editor-fold>
    # <editor-fold desc="获取网站链接">
    def get_web_url(self):
        current_url = self.driver.current_url
        return current_url

    # </editor-fold>
    # <editor-fold desc="判断按钮是否可用 可用Trule 不可用Flase">
    def button_enabled(self, btnEle):
        # btnEle = driver.find_element_by_css_selector('div.p-b.t-c button')
        flag = btnEle.is_enabled()
        return flag

    # </editor-fold>
    # <editor-fold desc="获取标签文本">
    def get_attribute(self, ele, attribute="textContent"):
        return ele.get_attribute(attribute)

    # </editor-fold>
    # <editor-fold desc="获取 drover 句柄">
    def get_handles(self):
        #
        # handle1 = driver.current_window_handle
        handles = self.driver.window_handles
        return handles

    # </editor-fold>
    # <editor-fold desc="刷新当前页">
    def refresh(self):
        self.driver.refresh()
        # driver.navigate().refresh()

    # </editor-fold>
    # <editor-fold desc="等待页面标签加载 XPATH">
    def wait_ele_jazai(self, XPATH):
        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located(
            (
                By.XPATH,
                XPATH
            )
        )
        )

    def wait_ele_xpath(self, XPATH):
        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located(
            (
                By.XPATH,
                XPATH
            )
        )
        )

    # </editor-fold>
    # <editor-fold desc="等待页面标签加载 Class">
    def wait_ele_class(self, Class):
        WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                Class
            )
        )
        )

    # </editor-fold>

    def send_key(self, XPATH, text):
        ele = self.driver.find_element(by=By.XPATH, value=XPATH)
        ele.send_keys(text)

    def click_ele(self, XPATH):
        ele = self.driver.find_element(by=By.XPATH, value=XPATH)
        ele.click()

    def get_ele(self, XPATH):
        return self.driver.find_element(by=By.XPATH, value=XPATH)

    def select_ele(self, XPATH, ):
        # d定位下拉框
        self.select = Select(self.driver.find_element(by=By.XPATH, value=XPATH))
        # #通过索引号,值从0开始，每一条option为一个索引
        # option1 =  self.select.select_by_index(0)
        # option2 =  self.select.select_by_index(2)
        # # 通过value值，每个option都会有的属性
        # option3 =  self.select.select_by_value("pdf")
        # option4 =  self.select.select_by_value("doc")
        # # 通过文本，直接通过选项的文本来定位
        # option5 =  self.select.select_by_visible_text("微软 Powerpoint (.ppt)")
        # option6 =  self.select.select_by_visible_text("RTF 文件 （.rtf)")
        # all_selected_options = self.select.all_selected_options  # 返回所有选中的选项
        # options = self.select.options  # f返回所有选项
        # first_selected_option = self.select.first_selected_option  # 返回该下拉框第一个选项
        #  self.select.deselect_by_index()  # 取消所有选项
        return self.select

    def close(self):
        self.driver.close()
        self.driver.quit()

    def alert(self, accept=True):
        text = self.driver.switch_to.alert.text
        if accept:
            self.driver.switch_to.alert.accept()
        return text

    def switch_to_iframe(self, XPATH):
        # 1、先切换到 iframe子页面
        iframe_node = self.driver.find_element(By.XPATH, XPATH)
        # iframe_node = self.driver.find_element(By.XPATH, '//*[@id="anony-reg-new"]/div/div[1]/iframe')
        # //*[@id="anony-reg-new"]/div/div[1]/iframe
        self.driver.switch_to.frame(iframe_node)  # 切换到 iframe子页面

    # <editor-fold desc="对整个页面截图">
    def get_screenshot_as_file(self, img_path):
        self.driver.get_screenshot_as_file(img_path)  # 对整个页面截图

    # </editor-fold>
    # 指定元素截图保存
    def get_screenshot_ele_as_png(self, ele, img_path):
        ele.screenshot(img_path)

    # 按下元素，并且不释放
    def click_and_hold(self, ele):
        ActionChains(self.driver).click_and_hold(ele).perform()  # 按下按钮

    # 选择ele指定位置进行点击操作
    def move_to_element_with_offset_click(self, ele, x, y):
        ActionChains(self.driver).move_to_element_with_offset(ele, int(x), int(y)).click().perform()

    # 按偏移量移动
    def move_by_offset(self, xoffset, yoffset=0):
        ActionChains(self.driver).move_by_offset(xoffset=xoffset, yoffset=yoffset).perform()

    # 流程释放鼠标
    def release(self):
        ActionChains(self.driver).release().perform()

    # 执行JavaScript来获取LocalStorage的内容
    def get_localStorage(self, key):
        localStorage_data = self.driver.execute_script(f"return window.localStorage.getItem('{key}')")
        return localStorage_data

    def get_localStorages(self):
        localStorage_data = self.driver.execute_script("return JSON.stringify(localStorage)")
        return localStorage_data

    def get_sessionStorages(self):
        localStorage_data = self.driver.execute_script("return JSON.stringify(sessionStorage)")
        return localStorage_data

    def get_sessionStorage(self, key):
        localStorage_data = self.driver.execute_script(f"return window.sessionStorage.getItem('{key}')")
        return localStorage_data

    def get_cookies(self):
        return self.driver.get_cookies()

    def user_agent(self):
        # 执行JavaScript来获取User-Agent
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        return user_agent

    # <editor-fold desc="滑动解锁">
    def slide_to_unlock(self, Xpath, move):
        try:
            # #获取元素
            # //*[@id="nc_1_n1z"]
            nc_1_n1z = self.driver.find_element(By.XPATH, Xpath)
            action = ActionChains(self.driver)
            # 鼠标左键按下不放
            action.click_and_hold(nc_1_n1z).perform()
            # 平行移动大于解锁的长度的距离
            #     拖动：
            # 1，drag_and_drop(soure=起始元素, target=结束元素)
            # 2，drag_and_drop_by_offset(soure=起始元素，xoffset，yoffset)，其中xoffset是水平便宜了，yoffset是垂直偏移量。
            action.drag_and_drop_by_offset(nc_1_n1z, move, 0).perform()
        except UnexpectedAlertPresentException as e:
            print(e)

    # </editor-fold>


class Captcha():
    def get_pos(self, imgsrc, img_w, img_h, w_error=10, h_error=10):
        img = cv2.imread(imgsrc)
        #
        bluu = cv2.GaussianBlur(img, (5, 5), 0, 0)
        cv2.imwrite(f'd/a_{int(time.time())}.jpg', bluu)

        canny = cv2.Canny(bluu, 0, 100)
        cv2.imwrite(f'd/b_{int(time.time())}.jpg', canny)
        contours, hi = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # 面积
            area = cv2.contourArea(contour)
            # 周长
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite(f'd/{int(time.time())}.jpg', img)
            z = cv2.arcLength(contour, True)
            if (img_w - w_error) * (img_h - h_error) < area < (img_w + w_error) * (img_h + h_error) and (
                    (img_w - w_error) + (img_h - h_error)) * 2 < z < ((img_w + w_error) + (img_h + h_error)) * 2:
                # if 5025 < area < 7225 and 300 < z < 380:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imwrite('111.jpg', img)
                return x
        return 0


# 验证码
class SeleniumCaptcha():
    # 爬虫模拟的浏览器头部信息
    # 根据位置对图片进行合并还原
    # filename:图片
    # location_list:图片位置
    # 内部两个图片处理函数的介绍
    # crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
    # paste函数的参数为(需要修改的图片，粘贴的起始点的横坐标，粘贴的起始点的纵坐标）

    # 滑动验证码案例
    def swipe_captcha(self):
        selen = SeleniumChromeUtil()
        selen.driver_url('https://accounts.douban.com')
        selen.click_ele('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]')
        selen.send_key('//*[@id="username"]', 'admin@qq.com')
        selen.send_key('//*[@id="password"]', 'admin')
        selen.click_ele('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a')
        selen.wait_ele_xpath('//*[@id="tcaptcha_iframe_dy"]')
        selen.switch_to_iframe('//*[@id="tcaptcha_iframe_dy"]')
        time.sleep(3)
        # 获取背景图片
        test1 = selen.get_attribute(selen.get_ele('//*[@id="slideBg"]'), 'style')
        p = r"background-image\s*:\s*url\((['\"]?)(.*?)\1\)"
        bigImageSrc = re.search(p, test1).group(2)
        urllib.request.urlretrieve(bigImageSrc, "bigImageSrc.PNG")
        slideBlock_l = selen.get_ele('//*[@id="slideBlock"]').size

        dis = Captcha().get_pos('bigImageSrc.PNG', slideBlock_l['width'], slideBlock_l['height'], )
        # 获取滑块的位置信息
        huak = selen.get_ele('//*[@id="tcOperation"]/div[6]')
        # 等比缩放，原图片的宽度为672，网页宽度为340，等比缩放
        dis = int(dis * 340 / 672 - huak.location['x'])
        ActionChains(selen.driver).click_and_hold(huak).perform()  # 按下按钮
        movie = 0
        while movie < dis:
            x = random.randint(3, 10)
            ActionChains(selen.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            movie += x
        ActionChains(selen.driver).release().perform()
        time.sleep(20)

    # 进度条验证码
    def mainprogress_bar(self, selen, XPATH):
        action = ActionChains(selen.driver)
        source = selen.get_ele(XPATH)  # 需要滑动的元素
        action.click_and_hold(source).perform()  # 鼠标左键按下不放
        action.move_by_offset(298, 0)  # 需要滑动的坐标
        action.release().perform()  # 释放鼠标
        time.sleep(0.1)
    # def
