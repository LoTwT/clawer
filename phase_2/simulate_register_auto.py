# 模拟登陆 - 人为识别验证码
# 中国科普博览网 http://auth.kepu.net.cn/user/login.html
import requests
from lxml import etree
import os
from utils.tujian import Tujian

base_url = "http://auth.kepu.net.cn/"
# 登录页面 url
login_url = "http://auth.kepu.net.cn/user/login.html"
# 登录请求 url
register_url = "http://auth.kepu.net.cn/user/weblogin.html"
# 首页 url
index_url = "http://auth.kepu.net.cn/index.html"

# 要保存的文件夹
save_folder = "register"

# 实例化 session, 建立长连接
session = requests.Session()


# 下载验证码图片
def download_captcha():
    login_response = session.get(url=login_url)
    html = etree.HTML(login_response.text)

    captcha_url = base_url + \
        html.xpath('//form[@id="weblogin"]/div[3]/div/div/img/@src')[0]

    check_folder(save_folder)

    with open(f"{save_folder}/captcha.jpg", "wb") as f:
        f.write(session.get(url=captcha_url).content)


# 检查文件夹是否存在
def check_folder(save_folder):
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)


# 用户输入
def get_user_info():
    username = str(input("请输入科普网用户名或邮箱: "))
    password = str(input("请输入科普网密码: "))

    tujian = Tujian()
    captcha = tujian.get_randomCode(f"{save_folder}/captcha.jpg")

    return username, password, captcha


# 请求登录
def register(username, password, captcha):
    data = (
        ("username", username),
        ("password", password),
        ("checkcode", captcha)
    )

    register_response = session.post(url=register_url, data=data)
    with open(f"{save_folder}/register.html", "w", encoding="utf-8") as f:
        f.write(register_response.text)

    check_response = session.get(url=index_url, allow_redirects=False)
    if check_response.status_code == 200:
        print("登陆成功")
    else:
        print("登录失败")


# 主函数
def run():
    download_captcha()
    username, password, captcha = get_user_info()
    register(username, password, captcha)


if __name__ == "__main__":
    run()
