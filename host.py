import socket
import multiprocessing
from multiprocessing import Process, Queue
from collections import 

def main(queue: Queue):
    message = input("Enter message: ")
    queue.put(message)

def communicate():
    # 服务器地址和端口
    SERVER_ADDRESS = ('localhost', 8000)
    # 创建Socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接到服务器
    client_socket.connect(SERVER_ADDRESS)
    print(f"Connected to server at {SERVER_ADDRESS}")

    while True:
        if len(queue) != 0:
            for q in queue:
                client_socket.send(q.encode())
            queue.empty()

    # return

    # while True:
    # # 发送消息
    # message = input("Enter message: ")
    # client_socket.send(message.encode())

    # # 接收服务器发送的消息
    # data = client_socket.recv(1024)
    # print(f"Received message from server: {data.decode()}")

    # # 关闭Socket连接
    # client_socket.close()


if __name__ == "__main__":
    queue = Queue()
    producer_process = Process(target=main, args=(queue,))
    consumer_process = Process(target=communicate, args=(queue,))

    producer_process.start()
    consumer_process.start()