import subprocess
from telnetlib import Telnet
import os
import wmi
import time
import re

host = "127.0.0.1"
port = 4444
name = 'openocd.exe'
name2 = 'python32.exe'
ti = 0;


''' regex for 1,2 and 4 bytes response '''
regex1b = re.compile(r"(0x[0-9a-fA-F]{8}):\s+([0-9a-fA-F]{2})")   # parse openocd response
regex2b = re.compile(r"(0x[0-9a-fA-F]{8}):\s+([0-9a-fA-F]{4})")   # parse openocd response
regex4b = re.compile(r"(0x[0-9a-fA-F]{8}):\s+([0-9a-fA-F]{8})")   # parse openocd response

def telnetsession():

    try:

        tn = Telnet()                                           # create Telnet object
        tn.set_debuglevel(100)                                    # set debug level to be verbose 
        tn.open(host, port)                                     # establish telnet connection
        ret1 = tn.read_until(b'\r\n\r> ').decode('utf-8')       # wait for response 

        ''' read loop example'''
        addr = 26608    # DieIDAddress from swim_conf database

        for count in range(0,4):
           
            command = r"mdb %d".encode('ascii') % (addr + count)
            tn.write(command + b'\r\n')
            time.sleep(0.1)
            res = tn.read_until(b'\r\n\r').decode('ascii')
            # print(res)

            searchObj = regex1b.search(res)
            if searchObj:
                resp = searchObj.group(2)
                print('byte recibido: ', resp)


    except:
        print("\n\nunable to connect to server\n\n")
        return



if __name__ == "__main__":


    f = wmi.WMI()
    for process in f.Win32_Process():
        if process.name == name or process.name == name2:
            process.Terminate()
            print("Openocd process terminated!\n\n")
            ti += 1

    if ti == 0:
        print("Openocd Process not found!!!\n\n")


    try:

        '''     openocd -f interface/stlink-dap.cfg -f target/stm8s105.cfg -c "init" -c "reset run"         '''
        subprocess.Popen(["openocd", "-f", "interface/stlink-dap.cfg", "-f", "target/stm8s105.cfg", "-c", "init", "-c", "reset"])
        time.sleep(4)
        telnetsession()

    except:
        pass