import os
import time

outfile_name = 'active.txt'

while(1):
    os.system("vboxmanage.exe list runningvms > " + outfile_name)
    time.sleep(1)
    with open(outfile_name) as f:
        cnt=0
        for line in f:
            cnt+=1
        if(cnt>0):
            print("acvive vms : " + str(cnt))
        
        