import socket

sock = socket.socket()
sock.connect(('localhost', 9092))

while True:
    data = sock.recv(1024)
    print(str(data, encoding="UTF-8"))
    if "your turn" in str(data, encoding="UTF-8"):
        u = input()
        sock.send(bytes(u, encoding='UTF-8'))
    if "good bye" in str(data, encoding="UTF-8"):
        break
sock.close()