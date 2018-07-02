#!/usr/bin/env python
#coding=utf-8

import socket
import re
import json
import sys
import cgi
import os

HOST = ''
PORT = 8000

#Read index.html, put into HTTP response data

#Read reg.html, put into HTTP response data

#Read picture, put into HTTP response data



#Configure socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(100)

d = {}
li = os.listdir(os.getcwd())#列出目录下的所有文件和目录
li2 = []
#print 'dirlist:',li
for i in range(len(li)):
    if  "vote-data"  in li[i]:
        li2.append(li[i])
print 'li2:',li2
li2.sort();
dir = li2[-1]
        
print 'dir:',dir


#infinite loop
while True:
    # maximum number of requests waiting
    conn, addr = sock.accept()
    request = conn.recv(1024)
    method = request.split(' ')[0]

    print 'Connect by: ', addr
    print 'Request is:\n', request
    
    #deal with GET method
    if method == 'GET':
        src  = request.split(' ')[1]
        nodename  = src.split('/?node=')[1]
        #nodename  = src.split('/')[1]
        for i in range(179):
            fname = "list" + str(i + 1) + ".txt"
            f = open(dir + "/" + fname)
            rows = json.load(f)
            #print 'nodename:',src,nodename
            for r in rows:
                if nodename in r['producers']:
                    # print r["owner"] + "   " + str(r["staked"]) + "  " + r["last_vote_weight"]
                    owner = r["owner"]
                    stacked = int(r["staked"])
                    d[owner] = stacked
        res = sorted(d.items(), key=lambda x: x[1], reverse=True)
        #print 'res:',str(res)
        for j in res:
            if int(j[1]) > 1000000000:
                print j[0] + "  " + str(j[1])
                

        
        #entry = form[-1]      # main content of the request
        entry = json.dumps(dict(res))
        #print(j)
        #entry = j 
        content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += entry
        content += '<br /><font color="green" size="7">register successs!</p>'
    

    #deal with POST method
    elif method == 'POST':
        #src  = request.split(' ')[1]
        #nodename  = src.split('/?node=')[1]
        nodename = request.get('node') 
        #form = cgi.FieldStorage()
        #print 'form:',form
        print 'nodename:',src,nodename
        for i in range(179):
            fname = "list" + str(i + 1) + ".txt"
            f = open(dir + "/" + fname)
            rows = json.load(f)
            for r in rows:
                if nodename in r['producers']:
                    # print r["owner"] + "   " + str(r["staked"]) + "  " + r["last_vote_weight"]
                    owner = r["owner"]
                    stacked = int(r["staked"])
                    d[owner] = stacked


        res = sorted(d.items(), key=lambda x: x[1], reverse=True)
        print 'res:',str(res)
        for j in res:
            if int(j[1]) > 1000000000:
                print j[0] + "  " + str(j[1])

        
        #entry = form[-1]      # main content of the request
        #j = json.loads(str(res))
        entry = json.dumps(dict(res))
        #print(j)
        #entry = j
        content = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n\r\n'
        content += entry
        content += '<br /><font color="green" size="7">register successs!</p>'
    
    ######
    # More operations, such as put the form into database
    # ...
    ######
    
    else:
        continue

    conn.sendall(content)
    
    #close connection
    conn.close()



