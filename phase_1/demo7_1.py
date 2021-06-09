# 代理 IP 使用
# 初体验

import requests
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions

# 确认本机 IP
# r = requests.get(url = 'https://httpbin.org/get').json()
# print(r)


# 使用代理 IP
# https://ip.jiangxianli.com/
# 把代理IP封装到字典中，和伪装请求头操作如出一辙
# proxies = {'http': 'http://202.61.51.204:3128',
#            'https': 'https://202.61.51.204:3128'}
# 然后在get的参数中把上面定义的proxies参数带上
# r = requests.get('http://httpbin.org/get', proxies=proxies).json()
# print(r)


# 使用 Selenium 发起使用代理 IP 的请求
options = ChromeOptions()

proxy = 'http://202.61.51.204:3128'

options.add_argument(('--proxy-server=' + proxy))
driver = webdriver.Chrome(options=options)
driver.get('http://httpbin.org/get')

time.sleep(3)

print(driver.page_source)    # 打印响应数据

driver.quit()
