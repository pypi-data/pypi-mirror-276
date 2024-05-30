from anon_traffic.utils import (
    generate_aes_key,
    IpdotPort2Ip_Port,
)
from cryptography.fernet import Fernet


# 解密函数
def disanon(key, ip_port):
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


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Decrypt anon traffic data.")
    parser.add_argument("key", type=str, help="The decryption key")
    parser.add_argument("anon_data", type=str, help="The anonymized data")
    args = parser.parse_args()

    ip, port = disanon(args.key, args.anon_data)
    return ip, port


if __name__ == "__main__":
    main()
