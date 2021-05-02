# 模拟登陆
# selenium

from selenium import webdriver
from tujian import Tujian
import time

login_url = "https://www.okcis.cn/login/"

chrome = webdriver.Chrome()
chrome.get(login_url)

username = str(input("请输入招标采购网账号: "))
password = str(input("请输入招标采购网密码: "))

# 识别验证码
chrome.find_element_by_xpath(
    '//*[@id="zhanghaocheck"]//img[@id="setcode"]').screenshot("./randomCode.png")
tujian = Tujian()
randomCode = tujian.get_randomCode("./randomCode.png")

time.sleep(1)
# 输入账号
chrome.find_element_by_xpath(
    '//*[@id="zhanghaocheck"]//input[@id="uname"]').send_keys(username)

time.sleep(1)
# 输入密码
chrome.find_element_by_xpath(
    '//*[@id="zhanghaocheck"]//input[@id="pwd"]').send_keys(password)

time.sleep(1)
# 输入验证码
chrome.find_element_by_xpath(
    '//*[@id="zhanghaocheck"]//input[@id="yzm"]').send_keys(randomCode)

time.sleep(1)
# 点击登录
chrome.find_element_by_xpath(
    '//*[@id="zhanghaocheck"]//input[@name="Submit"]').click()

time.sleep(2)
chrome.quit()
