"""
    电子词典服务端
"""
import sys
from multiprocessing import Process
from socket import socket
from signal import *
from time import time, sleep

# 调用dict_db.py中的类
from dict_db import Database


def login(connfd, name, passwd):
    # 查询数据库观察用户是否已经注册合法
    # 实例化数据库操作对象
    database = Database()
    # 调用Database中的方法
    sig = database.login(name, passwd)
    print(name, passwd)
    if not sig:
        connfd.send(b"NO")
        return
    connfd.send(b"OK")


def register(connfd, name, passwd):
    # 实例化数据库操作对象
    database = Database()
    # 调用Database中的方法
    sig = database.register(name, passwd)
    if not sig:
        connfd.send(b"NO")
        return
    connfd.send(b"OK")


def save_hist(connfd, word, name):
    # 实例化数据库操作对象
    database = Database()
    # 调用Database中的方法
    database.save_hist(word, name)


def query_word(connfd, word, name):
    # 实例化数据库操作对象
    database = Database()
    # 调用Database中的方法
    meaning = database.query_word(word)
    connfd.send(meaning.encode())
    # 保存用户查询的历史记录
    save_hist(connfd, word, name)


def get_hist(connfd, name):
    # 实例化数据库操作对象
    database = Database()
    # 调用Database中的方法
    # 循环发送查询到的历史信息
    result = database.get_hist(name)

    for ele in result:
        msg = '%s %s %s' % ele
        connfd.send(msg.encode())
        # 延时防止tcp粘包
        sleep(0.1)
    # 发送结束标志
    connfd.send(b"finsh")


class MyProcess(Process):
    def __init__(self, connfd=None):
        super().__init__()
        self.connfd = connfd

    def run(self):
        while True:
            msg = self.connfd.recv(1024).decode()
            if not msg or msg == 'E':
                self.connfd.close()
                break
            msg = msg.split(' ')
            # 分类讨论
            if msg[0] == 'R':
                register(self.connfd, msg[1], msg[2])
            elif msg[0] == 'L':
                login(self.connfd, msg[1], msg[2])
            elif msg[0] == 'Q':
                query_word(self.connfd, msg[1], msg[-1])
            elif msg[0] == 'H':
                get_hist(self.connfd, msg[1])


def main():
    # 创建tcp套接字
    tcp_sock = socket()
    # 绑定服务端地址
    tcp_sock.bind(('0.0.0.0', 8888))
    # 设置监听
    tcp_sock.listen(5)
    # 处理僵尸
    signal(SIGCHLD, SIG_IGN)

    while True:
        try:
            # 等待处理客户端链接
            print("等待客户端链接...")
            connfd, addr = tcp_sock.accept()
            print("Connect from ", addr)
        except KeyboardInterrupt:
            tcp_sock.close()
            sys.exit("服务端退出...")

        # 为每一个连接的客户端创建独立的进程
        p = MyProcess(connfd=connfd)
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
