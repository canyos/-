import os
import time

outfile_name = 'cpu.txt'
time_threshold = 5
cpu_threshold = 70
cnt =0
check_interval = 1
os.system("vboxmanage.exe metrics setup kali Guest/CPU/Load")
time.sleep(7)

while(1):
    try:
        os.system("VBoxManage.exe metrics query kali Guest/CPU/Load/User > " + outfile_name )
        time.sleep(check_interval)
        with open(outfile_name) as f:
            for line in f:
                pass
            #print(line)
            percentage_str = line.split()[2]
            percentage_float = float(percentage_str.rstrip('%'))
            print(percentage_float)

        if(percentage_float > cpu_threshold):
            cnt+=1
        else :
            cnt=0
    except:
        time.sleep(1)
        
    if(cnt>=time_threshold):
        os.system("VBoxManage.exe controlvm kali poweroff ")
        print("vm off")
        
        os.system("VBoxManage.exe clonevm --register kali --name kali(clone)")
        print("vm clone")
        
        os.system("VBoxManage.exe startvm kali  ")
        print("vm start")
        
        os.system("VBoxManage.exe startvm kali(clone) ")
        print("vm clone start")

        os.system("vboxmanage.exe metrics setup kali Guest/CPU/Load")
        time.sleep(7)
        
        