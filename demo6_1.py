# 模拟登录
# 人工识别验证码
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
    randomCode = str(input("请输入验证码: "))

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


if __name__ == "__main__":
    # 实例化一个 session
    s = requests.session()

    # 获得验证码
    get_randomCode(randomCode_url)

    # 模拟登陆
    post_login_info()
