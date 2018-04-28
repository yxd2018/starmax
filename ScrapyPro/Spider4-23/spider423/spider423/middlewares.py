# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  #支持的定位器分类
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import time
from spider423 import settings
import random
from pyvirtualdisplay import Display
import json

class Spider423SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Spider423DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    def __init__(self, timeout=None):
        # self.display = Display(visible=0, size=(1400, 700))
        # self.display.start()

        self.ua = random.choice(settings.MY_USER_AGENT)
        self.ip = random.choice(settings.IPPOOL)
        print(self.ip)
        print(self.ua)
        self.logger = getLogger(__name__)
        self.timeout = timeout

        # 进入浏览器设置
        self.options = webdriver.ChromeOptions()
        # 设置中文
        self.options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        self.options.add_argument(
            # 'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"'
            'user-agent=%s'%self.ua
            )
        # 添加ip代理
        # self.options.add_argument("--proxy-server=%s"%self.ip)
        # self.options.add_argument("--proxy-server=http://34.227.82.35:8080")
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)#等待时间 两个参数 一个浏览器  一个时间


    def __del__(self):
        print('*******************************************')
        self.browser.quit()
        # self.display.stop()
    def process_request(self, request, spider):
        """
        Chrome抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        print('Chrome is Starting')
        print(request.url)

        try:
            self.browser.get(request.url)

        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
        else:
            # 判断元素是否可以点击
            login = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="nav-link-yourAccount"]')))
            # 单击登录
            login.click()
            time.sleep(5)

            # 输入用户名密码
            # 一个符合条件的元素加载进来即可
            input1 = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="ap_email"]')))
            input2 = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="ap_password"]')))
            input1.clear()
            input2.clear()
            input1.send_keys("18562557397")
            input2.send_keys("123456")
            # 判断元素是否可以点击
            submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="signInSubmit"]')))
            submit.click()

            # 获取cookie并通过json模块将dict转化成str
            dictCookies = self.browser.get_cookies()
            jsonCookies = json.dumps(dictCookies)
            # 登录完成后，将cookie保存到本地文件
            with open('cookies.json', 'w') as f:
                f.write(jsonCookies)

            for cookie in self.browser.get_cookies():
                print("%s=%s" % (cookie['name'], cookie['value']))

            self.browser.get_screenshot_as_file("test2.png")
            print(request.url)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)

    @classmethod
    def from_crawler(cls, crawler,):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
