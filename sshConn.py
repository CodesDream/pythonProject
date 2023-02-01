#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import paramiko
import urllib.request
import time
import requests


def get_external_ip():
    try:
        external_ipaddr = requests.get("http://jsonip.com/").json().get('ip')
        return external_ipaddr
    except:
        return None


def conn_dev(hostname: object, port: object, username: object, password: object, external_ip: object) -> object:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    print(time.strftime('%Y-%m-%d %H:%M:%S'), '当前公网地址：', external_ip)
    print(hostname, '已连接网络设备')

    if external_ip == "180.169.94.252":
        command = ssh.invoke_shell()
        command.send('sys\n')
        command.send('nat address-group addresspool\n')
        command.send('undo section 0\n')
        command.send('section 180.169.94.253 180.169.94.253\n')
        command.send('return\n quit\n')
    elif external_ip == "180.169.94.253":
        command = ssh.invoke_shell()
        command.send('sys\n')
        command.send('nat address-group addresspool\n')
        command.send('undo section 0\n')
        command.send('section 180.169.94.252 180.169.94.252\n')
        command.send('return\n quit\n')
    else:
        pass

    time.sleep(10)
    output = command.recv(65535)
    print(output.decode().strip())
    ssh.close()


if __name__ == '__main__':
    url = 'https://docker.io/'
    ip = "192.168.100.1"
    port = 22
    username = "admin"
    password = "g3z&ZKwU4"

    while True:
        external_ip = get_external_ip()

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]

        try:
            opener.open(url)
            print(url + '此链接访问正常')
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '当前公网地址：', external_ip)
            time.sleep(2)
        except urllib.error.HTTPError:
            print(url + '此链接不能访问')
            time.sleep(2)
            conn_dev(ip, port, username, password, external_ip)
            print('公网地址已自动更改，当前ip地址为：', external_ip)
        except urllib.error.URLError:
            print(url + '此链接不能访问')
            time.sleep(2)
            conn_dev(ip, port, username, password, external_ip)
            print('公网地址已自动更改，当前ip地址为：', external_ip)

        time.sleep(800)
