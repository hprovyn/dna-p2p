# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 07:16:09 2018

@author: hunte
"""

import sys
import py2p


myport = int(sys.argv[1])
connport = int(sys.argv[2])

print(myport, connport)
conn = py2p.MeshSocket("0.0.0.0", myport)
conn.connect("0.0.0.0", connport)

done = False

SNPs = ["Z631","M241", "L283"]

REPLY_TYPE = 2
QUERY_TYPE = 0

while done is not True:    
    msg = conn.recv()
    if msg is not None:
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
            
conn.close()