import socket

def main():
    host = socket.gethostname()
    port = 4000         # port of server_socket

    c_socket = socket.socket()
    c_socket.connect((host, port))
    message = input('NU DAVA: ')

    while message.lower().strip() != 'exit':
        c_socket.send(message.encode())
        msg = c_socket.recv(1024).decode()
        print(f'recieve msg in c_socket: {msg}')  
        message = input('NU DAVA: ')

    c_socket.close()


if __name__ == '__main__':
    main()

    