# This is a sample Python script.
import socket
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def first_socket()->None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("google.com" , 80))
        s.sendall(b"GET / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\nConnection: close\r\n\r\n")

        while True:

            data = s.recv(1024)

            if not data:
                break

            print(data.decode())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    first_socket()


