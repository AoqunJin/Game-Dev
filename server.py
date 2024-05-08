import socket
import threading

# 服务器地址和端口
SERVER_ADDRESS = ('192.168.182.57', 8000)

# 存储已连接客户端的列表
clients = []

# 创建Socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器地址和端口
server_socket.bind(SERVER_ADDRESS)

# 开始监听
server_socket.listen(5)
print(f"Server listening on {SERVER_ADDRESS}")

def broadcast(message, sender):
    """向所有客户端广播消息"""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client, address):
    """处理单个客户端的连接"""
    print(f"New connection from {address}")
    clients.append(client)

    while True:
        try:
            # 接收客户端发送的消息
            message = client.recv(1024)
            if not message:
                break
            print(f"Received message from {address}: {message.decode()}")

            # 将消息广播给其他客户端
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

    print(f"Connection closed from {address}")

# 主循环
while True:
    # 接受新的客户端连接
    client_socket, client_address = server_socket.accept()

    # 为新客户端创建一个新线程
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()