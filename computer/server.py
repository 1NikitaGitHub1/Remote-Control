import socket
import pyautogui

SPEED = 10

def handle_client(client_socket) -> None:
    """Handling the client's commands."""
    # Словарь команд и соответствующих функций
    commands = {
        "shutdown": lambda: client_socket.send("Close connection".encode('utf-8')) or "BREAK",
        "clc": lambda: pyautogui.click(),
        "up": lambda: pyautogui.moveRel(0, -SPEED),
        "bottom": lambda: pyautogui.moveRel(0, SPEED),
        "left": lambda: pyautogui.moveRel(-SPEED, 0),
        "right": lambda: pyautogui.moveRel(SPEED, 0),
    }

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Get command: {data}")

        action = commands.get(data, lambda: client_socket.send(f"The command {data} accept.".encode('utf-8')))
        result = action()  # Выполняем действие из словаря

        if result == "BREAK":  # Если команда "shutdown", завершаем цикл
            break

    client_socket.close()

def start_server(host='0.0.0.0', port=5050) -> None:
    """Start server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server listen on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
