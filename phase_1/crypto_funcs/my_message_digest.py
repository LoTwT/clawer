# 信息摘要算法
# 单向、每种算法得到加密结果的长度固定
# MD5     128bit => 32位十六进制
# SHA1    160bit => 40位十六进制
# SHA256  256bit => 64位十六进制
# SHA512  512bit => 128位十六进制
# ...

import hashlib


# MD5
def encrypt_MD5(data, salt=""):
    if type(data) != bytes:
        encode_bytes = data.encode()
    else:
        encode_bytes = data
    hash = hashlib.md5(encode_bytes)
    hash.update(salt.encode())
    hash_hex = hash.hexdigest()
    return hash_hex


# SH1
def encrypt_SHA1(data, salt=""):
    if type(data) != bytes:
        encode_bytes = data.encode()
    else:
        encode_bytes = data
    hash = hashlib.sha1(encode_bytes)
    hash.update(salt.encode())
    hash_hex = hash.hexdigest()
    return hash_hex


# SH256
def encrypt_SHA256(data, salt=""):
    if type(data) != bytes:
        encode_bytes = data.encode()
    else:
        encode_bytes = data
    hash = hashlib.sha256(encode_bytes)
    hash.update(salt.encode())
    hash_hex = hash.hexdigest()
    return hash_hex


# SH512
def encrypt_SHA512(data, salt=""):
    if type(data) != bytes:
        encode_bytes = data.encode()
    else:
        encode_bytes = data
    hash = hashlib.sha512(encode_bytes)
    hash.update(salt.encode())
    hash_hex = hash.hexdigest()
    return hash_hex


if __name__ == "__main__":
    data = 'Test string!'
    salt = "SALT"
    print(
        f"data: {data}, md5: {encrypt_MD5(data, salt)}, len: {len(encrypt_MD5(data, salt))}")
    print(
        f"data: {data}, sha1: {encrypt_SHA1(data, salt)}, len: {len(encrypt_SHA1(data, salt))}")
    print(
        f"data: {data}, sha256: {encrypt_SHA256(data, salt)}, len: {len(encrypt_SHA256(data, salt))}")
    print(
        f"data: {data}, sha512: {encrypt_SHA512(data, salt)}, len: {len(encrypt_SHA512(data, salt))}")
