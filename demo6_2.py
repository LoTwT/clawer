import base64
import json
import requests


# 模拟登录
# 第三方平台识别
# 古诗文网 https://so.gushiwen.cn/user/login.aspx

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

randomCode_url = "https://so.gushiwen.cn/RandCode.ashx"
login_url = "https://so.gushiwen.cn/user/login.aspx"


# 下载验证码图片
def get_randomCode(randomCode_url):
    randomCode_response = requests.get(randomCode_url, headers=headers)

    with open("./randomCode.png", "wb") as f:
        f.write(randomCode_response.content)


# post 提交表单
def post_login_info():
    username = str(input("请输入您的帐号: "))
    password = str(input("请输入您的密码: "))

    # 在此处填入图鉴平台的帐号密码
    tujian = Tujian(tujianUsername, tujianPassword, 3)
    randomCode = tujian.get_randomCode("./randomCode.png")

    # 拼装表单数据
    login_data = {
        "__VIEWSTATE": "scRYmYFhUorSl0k1ZjEuZ0iApHMx9OhHgeA6N5v6ewiF8PGF5q/cFenk+g6iRi+XkMZYBOginoZ8HjeGehIzMTMdieTHac2DsJnNkFy405JJKa/T/TLYUAx9drs=",
        "__VIEWSTATEGENERATOR": "C93BE1AE",
        "email": username,
        "pwd": password,
        "code": randomCode.upper(),
        "denglu": "登录"
    }

    login_response = requests.post(login_url, headers=headers, data=login_data)
    if login_response.status_code == 200:
        print("登录成功")
    else:
        print("登录失败")


class Tujian:
    # 一、图片文字类型(默认 3 数英混合)：
    # 1 : 纯数字
    # 1001：纯数字2
    # 2 : 纯英文
    # 1002：纯英文2
    # 3 : 数英混合
    # 1003：数英混合2
    #  4 : 闪动GIF
    # 7 : 无感学习(独家)
    # 11 : 计算题
    # 1005:  快速计算题
    # 16 : 汉字
    # 32 : 通用文字识别(证件、单据)
    # 66:  问答题
    # 49 :recaptcha图片识别 参考 https://shimo.im/docs/RPGcTpxdVgkkdQdY
    # 二、图片旋转角度类型：
    # 29 :  旋转类型
    #
    # 三、图片坐标点选类型：
    # 19 :  1个坐标
    # 20 :  3个坐标
    # 21 :  3 ~ 5个坐标
    # 22 :  5 ~ 8个坐标
    # 27 :  1 ~ 4个坐标
    # 48 : 轨迹类型
    #
    # 四、缺口识别
    # 18：缺口识别
    # 五、拼图识别
    # 53：拼图识别

    def __init__(self, username, password, typeid):
        self.typeid = typeid
        self.username = username
        self.password = password

    def get_randomCode(self, img_path):
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
        data = {"username": self.username, "password": self.password,
                "typeid": self.typeid, "image": b64}
        result = json.loads(requests.post(
            "http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]


if __name__ == "__main__":
    # 实例化一个 session
    s = requests.session()

    # 获得验证码
    get_randomCode(randomCode_url)

    # 模拟登陆
    post_login_info()
