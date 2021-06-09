# BASE64
import base64


# base64 加密
def encrypt_base64(data):
    bytes_text = data.encode()  # 默认 utf-8 编码, 转换成 bytes
    b64_encode = base64.b64encode(bytes_text)
    return b64_encode  # 此处是 bytes


# base64 解密
def decrypt_base64(data):
    b64_decode = base64.b64decode(data)  # 此处是 bytes
    return b64_decode.decode(encoding="utf-8")


if __name__ == "__main__":
    data = "Test string!"
    encrypt_result = encrypt_base64(data)
    decrypt_result = decrypt_base64(encrypt_result)
    print(f"加密: {data}, encode: {encrypt_result}")
    print(f"解密: {encrypt_result}, decode: {decrypt_result}")
