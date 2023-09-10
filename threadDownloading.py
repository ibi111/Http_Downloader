import socket
import threading
from threading import Lock
import os
import time
lock=Lock()

class threadForDownloading(threading.Thread):

   def __init__(self, startingByte, endingByte,threadNumber,HOST,Directory,TimeToReportAfter,resume):
      threading.Thread.__init__(self)
      self.startingByte=startingByte
      self.endingByte=endingByte
      self.threadNumber=threadNumber
      self.HOST=HOST
      self.Directory=Directory
      self.TimeToReportAfter=TimeToReportAfter
      self.resume=resume

   def run(self):

      print("\n\nENDING BYTES OF THREAD"+str(self.threadNumber)+" = "+str(self.endingByte))
      print("\n\n")

      bytesDownloaded=0

      exists = os.path.isfile('C:\\Users\\Furqan\\Desktop\\cnProject\\PRACTICE_NO_OF_BYTES_WRITTEN by THREAD '+str(self.threadNumber)+'.txt')

      if exists:

          f=open("C:\\Users\\ibi\\Desktop\\Furqan\\PRACTICE_NO_OF_BYTES_WRITTEN by THREAD"+str(self.threadNumber)+".txt","r+")

          if self.resume==False:
              bytesDownloaded=0
              f.truncate(0)
          else:
              f.seek(0)
              bytesDownloaded=int(f.read())

      else:

          f=open("C:\\Users\\Furqan\\Desktop\\cnProject\\PRACTICE_NO_OF_BYTES_WRITTEN by THREAD"+str(self.threadNumber)+".txt","w+")

          f.seek(0)
          f.write('0')
          bytesDownloaded=0
          print(bytesDownloaded)

      global TOTAL_DOWNLOADED_BYTES

      lock.acquire()
      TOTAL_DOWNLOADED_BYTES += bytesDownloaded
      lock.release()

      time.sleep(2)

      global TOTAL_SPEED

      print("\nStarting Thread\n")

      filenameToDownloadTo="C:\\Users\\Furqan\\Desktop\\cnProject\\test"+str(self.threadNumber)+".txt"

      self.startingByte += bytesDownloaded

      r2="GET "+self.Directory+" HTTP/1.1\r\nHost:"+self.HOST+":80\r\nRange: bytes="+str(self.startingByte)+"-"+str(self.endingByte)+"\r\n\r\n\r\n"

      print(r2)
      print("\n\n")

      socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      socket1.connect((self.HOST,80))
      socket1.send(r2.encode('utf-8'))

      ignore_HTTP_header_response=True

      TIME_TRACKER=time.time()

      with open(filenameToDownloadTo, 'a+') as file_to_write:

          if self.resume==True:

              file_to_write.seek(int(bytesDownloaded))

          else:
               file_to_write.truncate(0)

          print('\nFILE OPENED\n')

          while True:

              start=time.time()
              data = socket1.recv(1000000)
              end=time.time()

              lock.acquire()
              TOTAL_DOWNLOADED_BYTES+=len(data)
              lock.release()

              if ignore_HTTP_header_response==True:
                  ignore_HTTP_header_response=False
                  data= data.decode('utf-8').split('\r\n\r\n')[1]
                  file_to_write.write(str(data))
                  bytesDownloaded+=len(data)
                  f.seek(0)
                  f.write(str(bytesDownloaded))
                  print("Bytes downloaded by thread "+str(self.threadNumber)+" =  "+str(bytesDownloaded))

              else:
                  if not data:
                      print("NO MORE DATA FOR THREAD "+str(self.threadNumber))
                      break

                  file_to_write.write(str(data.decode('utf-8')))
                  bytesDownloaded+=len(data)
                  f.seek(0)
                  f.write(str(bytesDownloaded))
                  #print("SLEEPING")
                  time.sleep(1)

              if time.time()-TIME_TRACKER >= self.TimeToReportAfter:
                  if end-start==0:
                      continue
                  else:
                      speed=(((len(data))/(end-start))/(1024))
                      print("\n"+str(self.threadNumber)+" Thread : has DOwnloaded bytes  = "+str(bytesDownloaded)+" / "+str(self.endingByte-self.startingByte+1)+" and has  Download speed in kb/s = "+ str(speed))
                      TIME_TRACKER=time.time()
                      TOTAL_SPEED+=speed

          print("CLOSING FILE")
          file_to_write.close()

      socket1.close()
      print("SOCKET CLOSED")

class threadForTotalDownloading(threading.Thread):
    def __init__(self,TimeToReportAfter,TOTAL_BYTES,resume):
        threading.Thread.__init__(self)
        self.TimeToReportAfter=TimeToReportAfter
        self.TOTAL_BYTES=TOTAL_BYTES
        self.resume=resume

    def run(self):

        TIME_TRACK=time.time()

        global TOTAL_SPEED
        global TOTAL_DOWNLOADED_BYTES

        if self.resume==True:
            time.sleep(2)
            print("BEFORE RESUMING TOTAL BYTES DOWNLOADED =  "+str(TOTAL_DOWNLOADED_BYTES))
            print("\n\n")

        while True:

            if TOTAL_DOWNLOADED_BYTES>=self.TOTAL_BYTES:
                break

            if time.time()-TIME_TRACK>= self.TimeToReportAfter:
                print("\nTOTAL :   DOWNLOADED = "+str(TOTAL_DOWNLOADED_BYTES)+" / "+str(self.TOTAL_BYTES)+ " and TOTAL DOWNLOAD SPEED in kb/s= "+str(TOTAL_SPEED)+"\n")
                TIME_TRACK=time.time()
                TOTAL_SPEED=0
