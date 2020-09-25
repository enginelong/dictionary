"""
    电子词典客户端
"""
from multiprocessing import Process
from socket import socket


# 创建自定义进程类


class Myclass:
    def __init__(self, sock=None):
        self.sock = sock

    def register(self, data, msg):
        name = data.split(' ')[0]
        msg = msg + ' ' + data
        self.sock.send(msg.encode())
        response = self.sock.recv(1024).decode()
        if response == 'OK':
            print("注册成功")
            self.login_next(name)
        else:
            print("注册失败")

    def login(self, data, msg):
        name = data.split(' ')[0]
        print(name)
        msg = msg + ' ' + data
        self.sock.send(msg.encode())
        response = self.sock.recv(1024).decode()
        if response == 'OK':
            print("登录成功")
            self.login_next(name)
        else:
            print("登录失败")

    def query_word(self, msg, name):
        while True:
            data = ''
            word = input("请输入想要查询的单词...")
            if word == '&&':
                break
            data = msg + ' ' + word + ' ' + name
            self.sock.send(data.encode())
            response = self.sock.recv(1024).decode()
            print("%s : %s"  % (word, response))


    def get_hist(self, msg, name):
        msg = msg + ' ' + name
        self.sock.send(msg.encode())
        # response => ((name, word, time))
        while True:
            response = self.sock.recv(1024).decode()
            if response == 'finsh':
                break
            print(response)

    def exit(self, msg):
        self.sock.send(msg.encode())
        print('谢谢使用')

    def login_next(self, name):
        while True:
            # 显示二级界面
            print("""
                *************** 登录界面 ***************
                   Q=>查询单词  H=>获取历史记录  E=>退出
                ***************************************
            """)

            msg = input("请输入命令> ")

            # 根据不同的请求执行不同的函数
            if msg == 'Q':
                self.query_word(msg, name)
            elif msg == 'H':
                self.get_hist(msg, name)
            elif msg == 'E':
                break
            else:
                print("请输入正确的指令...")


def main():
    # 创建tcp套接字
    tcp_sock = socket()
    # 链接服务端
    tcp_sock.connect(('127.0.0.1', 8888))

    # 为客户端创建实例化一个对象用于处理客户端的请求
    require = Myclass(tcp_sock)

    # 循环与服务器交互
    while True:
        # 显示一级界面
        print("""
            *************** 注册界面 ***************
                    R=>注册  L=>登录  E=>退出
            ***************************************
        """  )

        msg = input("请输入命令> ")

        # 根据不同的请求执行不同的函数
        if msg == 'R':
            data = input("请输入姓名和密码, 注意空格隔开> ")
            require.register(data, msg)
        elif msg == 'L':
            data = input("请输入姓名和密码, 注意空格隔开> ")
            require.login(data, msg)
        elif msg == 'E':
            require.exit(msg)
            break
        else:
            print("请输入正确的指令...")


if __name__ == '__main__':
    main()
