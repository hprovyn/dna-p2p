# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 07:16:09 2018

@author: hunte
"""

import py2p
import time
import pandas as pd
import datetime

myport = 4591
peerAddy = ""
debug_level = 0
query = ""
peerPort = ""
respondContactInfo = False
respondAncestorLatLon = False
respondAncestorBirthYear = False
contact = ""
ancestorLat = ""
ancestorLon = ""
ancestorBirthYear = ""

def getLogFileName():
    return "messages_" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".log"

logFileName = getLogFileName()

def getTimeString():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def writeToLogFile(message):
    f = open(logFileName, "a")
    f.write(getTimeString() + " " + message + "\r\n")
    f.close()
    
def readConfig():
    global myport
    global peerAddy
    global debug_level
    global query
    global peerPort
    global respondContactInfo
    global respondAncestorLatLon
    global respondAncestorBirthYear
    global contact
    global ancestorLat
    global ancestorLon
    global ancestorBirthYear
    
    a = pd.read_table("config.txt")
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
        if params[i] == "respondContactInfo":
            if vals[i] == "y" or vals[i] == "Y":
                respondContactInfo = True
        if params[i] == "respondAncestorLatLon":
            if vals[i] == "y" or vals[i] == "Y":
                respondAncestorLatLon = True
        if params[i] == "respondAncestorBirthYear":
            if vals[i] == "y" or vals[i] == "Y":
                respondAncestorBirthYear = True
        if params[i] == "contact":
            contact = vals[i]
        if params[i] == "ancestorLatitude":
            ancestorLat = vals[i]
        if params[i] == "ancestorLongitude":
            ancestorLon = vals[i]
        if params[i] == "ancestorBirthYear":
            ancestorBirthYear = vals[i]

readConfig()

conn = py2p.MeshSocket("0.0.0.0", myport, debug_level=debug_level, prot=py2p.base.Protocol('mesh', 'SSL'))

if peerAddy != "":
    conn.connect(peerAddy, peerPort)

done = False

STRs = {}

def getPrivacyCompliantResponse():
    response = []
    if respondContactInfo == True:
        response.append("contact=" + contact)
    if respondAncestorLatLon == True:
        response.append("lat=" + ancestorLat)
        response.append("lon=" + ancestorLon)
    if respondAncestorBirthYear == True:
        response.append("birthyear=" + ancestorBirthYear)
    return response


palindromic = ["DYS464"]

def readSTRs():
    a = pd.read_table("strs.txt")
    strNames = a["str"]
    allelles = a["allelle"]
    for i in range(len(strNames)):
        if strNames[i] in palindromic:
            inted = allelles[i]
        else:
            inted = int(allelles[i])
        STRs[strNames[i]] = inted


readSTRs()
print(STRs)
REPLY_TYPE = 2
QUERY_TYPE = 0

yesses = 0
received = 0
sent = False
time.sleep(3)

PALINDROMIC_DELIMITER = "-"

def palindromeHasValues(my_palindrome, values):
    for value in values:
        if value in my_palindrome:
            my_palindrome.remove(value)
        else:
            return False
    return True

def answerQuery(pairs):
    for pair in pairs:
        if "=" in pair:
            (the_str, the_allelle) = pair.split("=")
            if the_str in palindromic:
                thevals = STRs[the_str].split(PALINDROMIC_DELIMITER)
                the_alleles = the_allelle.split("-")
                phasvalues = palindromeHasValues(thevals, the_alleles)
                if phasvalues == False:
                    return False
            else:
                intallelle = int(the_allelle)
                print(the_str, the_allelle)
                if the_str not in STRs or STRs[the_str] != intallelle:
                    return False
        if "<" in pair:
            (the_str, the_allelle) = pair.split("<")
            
            intallelle = int(the_allelle)
            print(the_str, the_allelle)
            if the_str not in STRs or STRs[the_str] >= intallelle:
                return False
        if ">" in pair:
            (the_str, the_allelle) = pair.split(">")
            
            intallelle = int(the_allelle)
            print(the_str, the_allelle)
            if the_str not in STRs or STRs[the_str] <= intallelle:
                return False
    return True
   
while done is not True:    
    msg = conn.recv()
    if msg is not None:
        print(msg)
        msgtype = msg.packets[0]
        if msgtype == QUERY_TYPE:
            the_query = msg.packets[1]
            pairs = the_query.split(" and ")
            
            if answerQuery(pairs):
                response = getPrivacyCompliantResponse()
                responseString = "YES," + ",".join(response)
                msg.reply(responseString)
                writeToLogFile("replied " + responseString + " to query " + the_query)
            else:
                msg.reply("NO")
            print ("STATUS", conn.status)
        if msgtype == REPLY_TYPE:
            print(msg)
            the_response = msg.packets[1]
            if the_response.startswith("YES"):
                yesses += 1
                writeToLogFile("received " + the_response)
            received += 1
            print("received ", yesses, " YES", " out of ", received)
            

    if sent == False:
        conn.send(query)
        sent = True
        writeToLogFile("sent query " + query)
conn.close()