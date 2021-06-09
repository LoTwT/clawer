# js 逆向
# 有道翻译
import requests
import hashlib
import time
import random


class Translator:
    base_url = "https://fanyi.youdao.com/translate_o"
    # request headers
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "256",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID=2073044002@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=261049837.1651504; _ntes_nnid=a44707ab5effa81f0664b9745ae198f2,1618210880605; JSESSIONID=aaa_CfSTmsWwBb5XjEOLx; td_cookie=129571565; ___rl__test__cookies=1620981895777",
        "Host": "fanyi.youdao.com",
        "Origin": "https://fanyi.youdao.com",
        "Referer": "https://fanyi.youdao.com/",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    # query string params
    params = (
        ("smartresult", ["dict", "rule"]),
    )

    def __init__(self):
        self.target_word = str(input("请输入要翻译的内容: "))

    # 生成 lts => 生成 13 位时间戳
    def generate_lts(self):
        timestamp = int(time.time() * 1000)
        return str(timestamp)

    # 生成 salt => 时间戳 + 1 位 0 - 9 随机数
    def generate_salt(self, timestamp):
        return timestamp + str(random.randint(0, 9))

    # 生成 sign => md5 加密 "fanyideskweb" + e(要翻译的内容) + i(盐值) + "Tbh5E8=q6U3EXe+&L[4c@"
    def generate_sign(self, salt):
        return self.encrypt_md5("fanyideskweb" + self.target_word + salt + "Tbh5E8=q6U3EXe+&L[4c@")

    # 生成 bv => md5 加密 User-Agent
    def encrypt_md5(self, data):
        # 返回 md5 加密完成后的十六位信息摘要
        return hashlib.md5(data.encode()).hexdigest()

    # 组装 form_data
    def get_form_data(self):
        # 生成 lts
        lts = self.generate_lts()
        # 生成 salt
        salt = self.generate_salt(lts)
        # 生成 sign
        sign = self.generate_sign(salt)
        # 生成 bv => md5 加密 User-Agent
        bv = self.encrypt_md5(self.headers["User-Agent"])

        form_data = {
            "i": self.target_word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            "bv": bv,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_CLICKBUTTION",
        }
        return form_data

    # 发送请求, 获得翻译结果
    def request_translator(self):
        response = requests.post(
            url=self.base_url, headers=self.headers, params=self.params, data=self.get_form_data())
        print(response.json())


if __name__ == "__main__":
    translator = Translator()
    translator.request_translator()
