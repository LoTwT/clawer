# 对称加密算法 => AES
# 加密解密秘钥相同

import base64
from Crypto.Cipher import AES


# AES 加密, 密钥 key, 偏移量 iv, 模式默认 CBC
def encrypt_AES(data, key, iv="", mode=AES.MODE_CBC):
    # 填充字节函数
    def pad(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    # 填充字节
    data = pad(data)
    # 生成加密器
    cipher = AES.new(key.encode('utf8'), mode, iv.encode('utf8'))
    # 加密
    encrypted_bytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是 bytes 类型的数据
    # 使用 Base64 进行编码, 返回 byte 字符串
    encode_strs = base64.b64encode(encrypted_bytes)
    # 对byte字符串按utf-8进行解码
    enctext = encode_strs.decode('utf8')

    return enctext


# AES 解密, 秘钥 key, 偏移量 iv, 模式默认 CBC
def decrypt_AES(data, key, iv="", mode=AES.MODE_CBC):
    # 将加密数据转换位bytes类型数据
    if type(data) != bytes:
        encode_bytes = base64.decodebytes(data.encode('utf8'))
    else:
        encode_bytes = data
    # 生成加密器
    cipher = AES.new(key.encode('utf8'), mode, iv.encode('utf8'))
    # 解密
    decrypted_text = cipher.decrypt(encode_bytes)
    # 删除填充字节函数
    def unpad(s): return s[0:-s[-1]]
    # 删除填充字节
    decrypted_text = unpad(decrypted_text)
    decrypted_text = decrypted_text.decode('utf8')
    return decrypted_text


if __name__ == "__main__":
    key = 'handsomehandsome'  # 自己密钥
    data = 'hello maishu!'  # 需要加密的内容

    encrypted_text = encrypt_AES(data, key, iv="0102030405060708")
    print(encrypted_text)
    print(decrypt_AES(encrypted_text, key, iv="0102030405060708"))

    # 5iiemOvmLraVXcsZqIDs3A==    # 加密后的密文
    # hello maishu!               # 加密后的密文
