import socket
import sys
import re

BUFFER_SIZE=100000


def getContentLength(Host,directory):
    """
    :param Host: the source of the document [website/server]
    :param directory: location of the resource
    :return: length of content to be downloaded
    """
    socketHeader=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requestHeader="HEAD "+directory+" HTTP/1.1\r\nHost:"+Host+":80\r\n\r\n"

    socketHeader.connect((Host,80))

    socketHeader.send(requestHeader.encode('utf-8'))

    data = socketHeader.recv(100000)

    text = data.decode()

    contentLength = re.split('Content-Length:',text)[-1]

    contentLength=int(contentLength.splitlines()[0])

    socketHeader.close()

    return contentLength
def readCommandLineArguments():
    if len(sys.argv) == 10:
        if sys.argv[1] == '-r':
            resume_status=True

        num_of_connections=int(sys.argv[3])
        time=int(sys.argv[5])
        Host=str(sys.argv[7].split("/", 1)[0])
        Directory="/"+str(sys.argv[7].split("/", 1)[1])
        FilePathToDownloadTo=str(sys.argv[9])

        return resume_status,num_of_connections,time,Host,Directory,FilePathToDownloadTo

    elif len(sys.argv) == 9:
        resume_status=False
        num_of_connections=int(sys.argv[2])
        time=int(sys.argv[4])
        Host=str(sys.argv[6].split("/", 1)[0])
        Directory="/"+str(sys.argv[6].split("/", 1)[1])
        FilePathToDownloadTo=str(sys.argv[8])

        return resume_status,num_of_connections,time,Host,Directory,FilePathToDownloadTo

    else:
        print("Command line arguments not right")
        sys.exit(0)

def combineData(NUMBER_OF_THREADS,RESUMING_STATUS,FILE_LOCATION):
    """

    :param NUMBER_OF_THREADS: number of  threads downloading the file
    :param RESUMING_STATUS: resumed or not
    :param FILE_LOCATION: location of downloaded pieces
    :return:
    """

    print("\n\nFile is downloaded only writing\n\n")

    arrayOfFiles=[]

    for i in range(NUMBER_OF_THREADS):
        arrayOfFiles.append('C:\\Users\\ibi\\Desktop\\cnProject\\test'+str(i+1)+'.txt')

    with open(str(FILE_LOCATION)+'\\testAll.txt', 'wb+') as outfile:

        if RESUMING_STATUS==False:
            outfile.truncate(0)

        for fname in arrayOfFiles:
            with open(fname) as infile:
                outfile.write(infile.read().encode('utf-8'))

    print("WRITTEN")
