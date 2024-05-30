import hashlib
from datetime import datetime
import base64


def generate_aes_key(key_str, key_length=32):
    # 使用SHA-256哈希函数对输入的字符串密钥进行散列处理
    hashed_key = hashlib.sha256(key_str.encode()).digest()
    # 截取所需长度的哈希结果作为AES密钥
    aes_key = hashed_key[:key_length]
    aes_key = base64.urlsafe_b64encode(aes_key).decode()
    return aes_key


def timestamp2time(timestamp: str):
    # 将时间戳转换为整数
    timestamp = int(timestamp)

    # 使用datetime.fromtimestamp()方法将时间戳转换为具体的时间
    time = datetime.fromtimestamp(timestamp)
    return time


def IpdotPort2Ip_Port(ipdotport: str):
    # 找到最后一个点的索引
    last_dot_index = ipdotport.rfind(".")

    # 将字符串分成两部分，并替换最后一个点
    ip_port = ipdotport[:last_dot_index] + "_" + ipdotport[last_dot_index + 1 :]

    return ip_port
