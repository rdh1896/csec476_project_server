import socket
import sys

def main():
    host = "127.0.0.1"
    port = 25565
    print('# Creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    s.bind(server_address)
    s.listen(5)
    while True:
        print("Waiting for connection")
        connection, client = s.accept()
        try:
            while True:
                print("Connected to client IP: {}".format(client))
                command = input("$>").strip()
                connection.send(command.encode())
                if (command == "exit"):
                    break
                resp = connection.recv(4096).decode()
                print(resp)
        finally:
            connection.close()
            break
    s.close()

main()
