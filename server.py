import socket
import sys
import os

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(contents):
    with open("downloaded_file.txt", "w") as f:
        f.write(contents)

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
                elif (command == "upload_file"):
                    file = input("File to Upload (must be in server cwd): ")
                    file_contents = read_file(file)
                    connection.send(file_contents.encode())
                    resp = connection.recv(4096).decode()
                    print(resp)
                elif (command == "download_file"):
                    file = input("File to Download (must be in the client cwd, try uploaded_file.txt...): ")
                    connection.send(file.encode())
                    resp = connection.recv(4096).decode()
                    print("File Preview: " + resp[:9])
                    write_file(resp)
                    print("File written to server cwd")
                else:    
                    resp = connection.recv(4096).decode()
                    print(resp)
        finally:
            connection.close()
            break
    s.close()

main()
