# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 07:16:09 2018

@author: hunte
"""

import sys
import py2p
import time
import pandas as pd

myport = 4591
peerAddy = ""
debug_level = 0
query = ""
peerPort = ""

def readConfig():
    global myport
    global peerAddy
    global debug_level
    global query
    global peerPort
    
    a = pd.read_csv("config.txt")
    params = a["param"]
    vals = a["value"]
    for i in range(len(params)):
        print(params[i], vals[i])

        if params[i] == "port":
            myport = int(vals[i])
        if params[i] == "peerAddress" and str(vals[i]) != "nan":
            peerAddy = vals[i]
        if params[i] == "peerPort" and str(vals[i]) != "nan":
            print(vals[i], str(vals[i]))
            peerPort = int(vals[i])
        if params[i] == "debug":
            debug_level = int(vals[i])        
        if params[i] == "query":
            query = vals[i]

readConfig()

conn = py2p.MeshSocket("0.0.0.0", myport, debug_level=debug_level, prot=py2p.base.Protocol('mesh', 'SSL'))

if peerAddy != "":
    conn.connect(peerAddy, peerPort)

done = False

STRs = {}

def readSTRs():
    a = pd.read_csv("strs.txt")
    strNames = a["str"]
    allelles = a["allelle"]
    for i in range(len(strNames)):
        STRs[strNames[i]] = int(allelles[i])


readSTRs()
print(STRs)
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
            (the_str, the_allelle) = msg.packets[1].split("=")
            intallelle = int(the_allelle)
            print(the_str, the_allelle)
            if the_str in STRs and STRs[the_str] == intallelle:
                msg.reply("YES")
            else:
                msg.reply("NO")
            print("query for", intallelle)
            print ("STATUS", conn.status)
        if msgtype == REPLY_TYPE:
            print(msg)
            if msg.packets[1]=="YES":
                yesses += 1
            received += 1
            print("received ", yesses, " YES", " out of ", received)

    if sent == False:
        conn.send(query)
        sent = True
conn.close()