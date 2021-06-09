# 非对称加密算法 => RSA
# 公钥加密, 私钥解密。私钥解密, 公钥加密。
# RSA 公钥加密有类似 MD5 加盐的操作，所以相同的明文，用相同的公钥进行 RSA 加密可能会生成不同的密文

import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class MyRSA:
    def __init__(self):
        # 初始化RSA对象,  伪随机数生成器
        self.rsa = RSA.generate(1024, Random.new().read)
        # 生成公钥
        self.public_key = self.rsa.publickey().exportKey()
        # 生成私钥
        self.private_key = self.rsa.exportKey()

    # 加密
    def encrypt(self, data):
        pubkey = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(pubkey)
        return base64.b64encode(cipher.encrypt(data.encode('utf-8'))).decode('utf-8')

    # 解密
    def decrypt(self, data):
        prikey = RSA.importKey(self.private_key)
        cipher = PKCS1_v1_5.new(prikey)
        return cipher.decrypt(base64.b64decode(data), 'error').decode('utf-8')


if __name__ == "__main__":
    myrsa = MyRSA()

    text = 'hello maishu!'

    encrypt_text = myrsa.encrypt(text)
    print('加密后的密文：', encrypt_text)

    decrypt_text = myrsa.decrypt(encrypt_text)
    print('解密后的明文：', decrypt_text)
