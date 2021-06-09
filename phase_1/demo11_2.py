# JS 逆向
# http://jzsc.mohurd.gov.cn/data/company

import requests
from phase_1.crypto_funcs.my_aes import decrypt_AES
import binascii

base_url = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}
# 秘钥
key = "jo8j9wGw%6HbxfFn"
# 偏移量
iv = "0123456789ABCDEF"


# 根据要爬取的页数, 生成对应的请求参数的列表
def generate_params_list(page_counts):
    params_list = []
    for page_count in range(0, page_counts):
        params = (
            ("pg", page_count),
            ("pgsz", 15),
            ("total", 450)
        )
        params_list.append(params)
    return params_list


# 发送请求, 得到响应列表
def generate_response_list(params_list):
    response_list = []
    for params in params_list:
        response = requests.get(url=base_url, headers=headers, params=params)
        response_list.append(response)
    return response_list


# 解密数据
def decrypt(response_list):
    result = []
    for response in response_list:
        data = response.text
        # 将十六进制字符串转换为 bytes
        data = binascii.a2b_hex(data)
        decrypt_result = decrypt_AES(data=data, key=key, iv=iv)
        result.append(decrypt_result)
    return result


# 主函数
def run():
    page_counts = int(input("请输入要爬取的页数: "))
    params_list = generate_params_list(page_counts)
    response_list = generate_response_list(params_list)
    result = decrypt(response_list)
    print(f"共 {page_counts} 页:\n{result}")
    print(f"len(result): {len(result)}")


if __name__ == "__main__":
    run()
