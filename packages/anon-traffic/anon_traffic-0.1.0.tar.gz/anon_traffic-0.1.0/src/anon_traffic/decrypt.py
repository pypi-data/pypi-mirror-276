from anon_traffic.utils import (
    generate_aes_key,
    IpdotPort2Ip_Port,
)
import os
from cryptography.fernet import Fernet
from tqdm import tqdm


# 解密函数
def decrypt(key, ip_port):
    """
    输入被加密后的字符串
    输出ip, port
    """
    ip_port = ip_port.split(",")[-1].split("'")[-2]
    cipher_suite = Fernet(generate_aes_key(key))
    decrypted_ip_port = cipher_suite.decrypt(ip_port).decode()
    ip = ".".join(decrypted_ip_port.split(".")[:-1])
    port = int(decrypted_ip_port.split(".")[-1])
    return ip, port


if __name__ == "__main__":
    ip, port = decrypt(
        "iie12345",
        "b'gAAAAABmLonUtNuRAUmtoN-lYxXyQ1mx6ZgrAFmBEci3MLYikxMjbMp6tarGPHz_26p65jSCIdxhfyS43O4gsqMKQ8F4baG_0hl7QIl0rFeBPgj9u7tpEs4='",
    )
    print(ip)
    print(port)
