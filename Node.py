# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 08:25:22 2018

@author: hunte
"""

import sys
import py2p

myport = int(sys.argv[1])
outaddy = sys.argv[2]
outport = int(sys.argv[3])
connaddy = ""
connport = ""
if len(sys.argv) > 4:
    connaddy = sys.argv[4]
    connport = int(sys.argv[5])
print(myport, outaddy, outport)
conn = py2p.MeshSocket("localhost", myport, out_addr=(outaddy, outport))
print("protocol", conn.protocol)
print('created Node', myport)
if len(sys.argv) > 4:
    conn.connect(connaddy, connport)
done = False
while done is not True:
    done = False
conn.close()