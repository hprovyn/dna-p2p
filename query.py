# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 08:30:24 2018

@author: hunte
"""

import sys
import py2p
import time

myport = 4581
connport = 4591

query = sys.argv[1]

print(myport, connport, query)
conn = py2p.MeshSocket("0.0.0.0", myport)

conn.connect("localhost", connport)

time.sleep(5)
conn.send(query)

time.sleep(3)
REPLY_TYPE = 2

done = False

received = 0
yesses = 0
while done is not True:    
    msg = conn.recv()
    if msg is not None:
        msgtype = msg.packets[0]
        if msgtype == REPLY_TYPE:
            print(msg)
            if msg.packets[1]=="YES":
                yesses += 1
            received += 1
    else:
        done = True

print("received ", yesses, " YES", " out of ", received)