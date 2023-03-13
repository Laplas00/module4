import socket

def main():
    host = socket.gethostname()
    port = 4000
    s_socket = socket.socket()
    s_socket.bind((host, port))
    s_socket.listen()
    conn, address = s_socket.accept()
    print(f'connection from {address}, conn - {conn}')



    while True:
        # TCP дает нам именно баайты, поэтому их надо декодировать
        msg = conn.recv(1024).decode()
        if not msg:
            break
        else:
            print(f'message is {msg}')
        message = input('%: ')
        conn.send(message.encode())
    conn.close()
    s_socket.close()

    


if __name__ == "__main__":
    main()