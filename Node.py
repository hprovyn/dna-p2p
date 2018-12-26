# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 08:25:22 2018

@author: hunte
"""

import sys
import py2p


myport = int(sys.argv[1])
outaddy = ""
outport = ""
if len(sys.argv) > 2:
    outaddy = sys.argv[2]
    outport = int(sys.argv[3])
print(myport, outaddy, outport)

conn = py2p.MeshSocket("0.0.0.0", myport) #out_addr=(outaddy, outport))

if len(sys.argv) > 2:    
    conn.connect(outaddy, outport)
    
print("protocol", conn.protocol)
print('created Node', myport)
print(conn.status)
print(conn.id)
done = False
while done is not True:
    done = False
conn.close()