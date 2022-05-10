# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:10:00 2022

@author: Tsingh
"""

from socket import AF_INET, SOCK_DGRAM
import os
import socket
import struct, time
from datetime import datetime
import win32api
 
def getNTPTime(host = "192.168.10.123"):
        port = 5000
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
        t -= TIME1970
        #print(time.ctime(t),type(t))
        #return time.ctime(t).replace("  "," ")
        return t
def _win_set_time(time_tuple):
    
    dayOfWeek = datetime(*time_tuple).isocalendar()[2]
    t = time_tuple[:2] + (dayOfWeek,) + time_tuple[2:]
    win32api.SetSystemTime(*t)    

if __name__ == "__main__":
    a=getNTPTime()
    print(a)
    j=time.gmtime(a)[0:6] + (0,)
    #print(type(a))
    #Todays_date = date.today()
    #b = datetime.strptime(a)
    #print(j)
   # _win_set_time(j)
    #b=b.isocalendar()
    #print(b)
    #os.system('sudo date -s {}'.format(a))
    