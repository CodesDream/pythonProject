import paramiko
import time

username = "admin"
password = "Ujiabb.2020"
ip = "192.168.100.2"


def conn_dev():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username=username, password=password)
    print('已连接网络设备', ip)
    command = ssh.invoke_shell()
    command.send('sys\n')
    command.send('inter g0/0/24\n')
    command.send('port link-type access\n port default vlan 20\n ')
    command.send('dis current-configuration  interface GigabitEthernet 0/0/24\n')

    time.sleep(5)
    output = command.recv(65535)
    print(output.decode().strip())
    ssh.close()


if __name__ == '__main__':
    conn_dev()
