
from HelperFunctions import *
from uiHandler import *
from threadDownloading import  *
import math
import time

START_TIME=time.time()
TOTAL_DOWNLOADED_BYTES=0
TOTAL_SPEED=0


def main():
    ui = UI()
    path , url = ui.get_inputs()
    command =[path,url]

    RESUMING_STATUS,NUMBER_OF_THREADS,TIME,HOST,Directory,FilePathToDownloadTo=readCommandLineArguments(command)

    threads = []

    total=getContentLength(HOST,Directory)

    print("TOTAL BYTES TO DOWNLOAD = "+str(total))
    print("\n\n")

    division=total/NUMBER_OF_THREADS
    division=math.floor(division)

    start=0
    end=start+division-1

    thread = threadForTotalDownloading(TIME,total,RESUMING_STATUS)
    threads+= [thread]
    thread.start()

    for i in range(NUMBER_OF_THREADS):
        if((i+1)==NUMBER_OF_THREADS):
            end=total+BUFFER_SIZE
        thread = threadForDownloading(start,end,i+1,HOST,Directory,TIME,RESUMING_STATUS)
        threads += [thread]
        thread.start()
        start=end+1
        end=start+division-1

    for thread in threads:
        thread.join()

    combineData(NUMBER_OF_THREADS,RESUMING_STATUS,FilePathToDownloadTo)

main()
