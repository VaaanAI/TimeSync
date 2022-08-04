# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:10:00 2022

@author: Tsingh
"""

from socket import AF_INET, SOCK_DGRAM
import os
import socket
import struct, time
import subprocess
import json
# from datetime import datetime
# import win32api
 
def getNTPTime(host, port):
        host=host
        port = port
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'
 
        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800 # 1970-01-01 00:00:00
 
        # connect to server
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.sendto(msg.encode('utf-8'), address)
        msg, address = client.recvfrom( buf )
        #print(msg,type(msg))
        t = struct.unpack( "!12I", msg )[10]
        print("t: ", t)
        t -= TIME1970
        t1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        print("'"+t1+"'")
        return "'"+t1+"'"
        # print(time.ctime(t).replace("  "," "))
        # return time.ctime(t).replace("  "," ")
        #return t


if __name__ == "__main__":

    try:
        with open('Ubuntu_Client.json', 'r') as f:
            NTPConf = json.load(f)

        host_ip = NTPConf["HOST_IP"]
        port = NTPConf["Port"]

        print('Parameters set successfully.')

    except Exception as e:
        print('Error in reading json file.')


    a=getNTPTime(host_ip, port)
    # print('a: ', a)
#     os.system('sudo date --set={}'.format(a))
    # b = "'2021-07-20 14:58:14'"
    # cmd = "sudo date -s {}".format(a)
    # subprocess.run(cmd, shell=True, check=True)
    # os.system(cmd)
    os.system("sudo date -s {}".format(a))
    