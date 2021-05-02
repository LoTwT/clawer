# 模拟登陆
# requests

import requests
from tujian import Tujian


class Login:
    login_url = "https://www.okcis.cn/signed/"
    randomCode_url = "https://www.okcis.cn/php/checkUser/code.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }

    def __init__(self):
        # 实例化一个 session
        self.session_instance = requests.session()

    def pack_login_info(self):
        randomCode = self.calc_randomCode(self.randomCode_url)
        username = str(input("请输入招标采购网账号: "))
        password = str(input("请输入招标采购网密码: "))

        login_info = {
            "info[uname]": username,
            "info[pwd]": password,
            "info[yzm]": randomCode,
            "info[jzmm]": "1",
            "Submit": "(unable to decode value)"
        }

        return login_info

    def calc_randomCode(self, randomCode_url):
        randomCode_response = self.session_instance.get(
            url=randomCode_url, headers=self.headers)

        with open("./randomCode.png", "wb") as f:
            f.write(randomCode_response.content)

        tujian = Tujian()
        return tujian.get_randomCode("./randomCode.png")

    def do_login(self):
        login_info = self.pack_login_info()
        login_response = self.session_instance.post(
            url=self.login_url, headers=self.headers, data=login_info)

        if "账号管理" in login_response.text:
            print("登陆成功")
        else:
            print("登录失败")


if __name__ == "__main__":
    login = Login()
    login.do_login()
