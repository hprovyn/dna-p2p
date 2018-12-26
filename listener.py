# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 07:16:09 2018

@author: hunte
"""

import sys
import py2p
import time

myport = 4591

outaddy = ""

if len(sys.argv) > 1:
    outaddy = sys.argv[1]
    
print(outaddy)

conn = py2p.MeshSocket("0.0.0.0", myport, debug_level=5)

if outaddy != "":
    conn.connect(outaddy, 4591)

done = False

SNPs = ["Z631","M241", "L283"]

REPLY_TYPE = 2
QUERY_TYPE = 0

yesses = 0
received = 0
sent = False
time.sleep(3)
while done is not True:    
    msg = conn.recv()
    if msg is not None:
        print(msg)
        msgtype = msg.packets[0]
        if msgtype == QUERY_TYPE:
            snp = msg.packets[1]
            print(snp)
            if snp in SNPs:
                msg.reply("YES")
            else:
                msg.reply("NO")
            if snp == "shutdown":
                done = True
            
            print ("STATUS", conn.status)
        if msgtype == REPLY_TYPE:
            print(msg)
            if msg.packets[1]=="YES":
                yesses += 1
            received += 1
            print("received ", yesses, " YES", " out of ", received)

    if sent == False:
        conn.send("M241")
        sent = True
conn.close()