import socket
import re

BUFFER_SIZE=100000

def getContentLength(Host,directory):
    """
    :param Host: the source of the document [website/server]
    :param directory: location of the resource
    :return: length of content to be downloaded
    """
    contentLength=0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketHeader:
        requestHeader="HEAD "+directory+" HTTP/1.1\r\nHost:"+Host+":80\r\n\r\n"
        print(requestHeader)
        socketHeader.connect((Host,80))
        socketHeader.sendall(requestHeader.encode('utf-8'))

        data = socketHeader.recv(BUFFER_SIZE)
        text = data.decode()
        print(text)

        # contentLength = re.split('Content-Length:',text)[-1]
        # contentLength=int(contentLength.splitlines()[0])

    return 0

def tester():
    print(getContentLength("filesamples.com","/samples/document/txt/sample3.txt"))
tester()
