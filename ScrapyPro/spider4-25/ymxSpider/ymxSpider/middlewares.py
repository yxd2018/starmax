# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
# from logging import getLogger
from ymxSpider import settings
import random
import time
import json


class YmxspiderSpiderMiddleware(object):
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


class YmxspiderDownloaderMiddleware(object):
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


class YmxspiderseleniumMiddleware(object):
    def __init__(self,timeout=None):
        self.ua = random.choice(settings.MY_USER_AGENT)
        self.ip = random.choice(settings.IPPOOL)
        self.timeout = timeout

        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument('user-agent=%s'%self.ua)
        # self.browser_options.add_argument('--proxy-server=%s'%self.ip)
        # self.browser_options.add_argument('--headless')

        self.browser = webdriver.Chrome(chrome_options=self.browser_options)
        self.browser.set_window_size(1000, 900)
        self.wait = WebDriverWait(self.browser,self.timeout)

    def __del__(self):
        self.browser.quit()


    def process_request(self,request,spider):
        print('Chrome is Starting')
        print(request.url)

        self.browser.get(request.url)
        self.browser.delete_all_cookies()
        with open('cookie.json', 'r') as f:
            listCookies = json.loads(f.read())
            for cookie in listCookies:
                self.browser.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in cookie})


        try:
            self.browser.get(request.url)

        except TimeoutException,e:
            print(str(e))
            return HtmlResponse(url=request.url, status=500, request=request)
        else:
            """
            # 点击登录
            login = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="nav-link-yourAccount"]')))
            login.click()
            # 输入用户名密码
            input1 = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))

            input2 = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))

            input1.clear()
            input2.clear()

            input1.send_keys('18562557397')
            input2.send_keys('123456')

            submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="signInSubmit"]')))
            submit.click()

            # 记录cookie
            cookiedict = self.browser.get_cookies()
            cookiejson = json.dumps(cookiedict)

            with open('cookie.json', 'wb') as f:
                f.write(cookiejson)
            """
            # button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="a-button-input"]')))
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@id="click-to-chat-button"]')))
            button.click()
            self.browser.switch_to_window(self.browser.window_handles[1])
            try:
                pwd = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="ap_password"]')))
                pwd.send_keys('123456')
                print(pwd)
                bt_log = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="signInSubmit"]')))
                bt_log.click()
            except Exception,e:
                print(str(e)+"没有获取到密码")
            finally:
                textarea = self.wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@class="chat-cust-question"]')))
                textarea.send_keys(u"什么时间能发货?")
                sub = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="开始聊天"]')))
                sub.click()
                return HtmlResponse(url=request.url, status=200, body=self.browser.page_source, request=request)

    @classmethod
    def from_crawler(cls, crawler, ):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))