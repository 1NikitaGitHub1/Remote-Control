import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 5050))
server.listen()
print("Сервер запущен. Ожидание подключения...")

while True:
    client, address = server.accept()
    print(f"Подключение от {address}")
    while True:
        data = client.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Получено: {data}")
        client.send(f"Сервер получил: {data}".encode('utf-8'))
    client.close()