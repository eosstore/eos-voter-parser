# -*- coding: UTF-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import re
import sys
import os
import requests

def http_client(nodename):
    #url = 'https://vote.changshang15.com/v1/chain/get_producers'
    # url curl --request POST --url https://vote.changshang15.com/v1/chain/get_producers --data '{"limit":"100","json":"true"}'
    url = 'http://52.221.176.243:8889/v1/chain/get_producers'

    # Make a POST request and read the response
    headers = {'content-type': 'application/json'}
    data = json.dumps({"limit":"100","json":"true"})
    res = requests.post(url, data=data, headers=headers)
    #print(res.text)
   
    res = json.loads(res.text)
    for it in iter(res['rows']):
        if it['owner'] == nodename:
            #print it
            return it

def search_name(nodename):
    d = {}
    li2 = []
    #get  vote-data
    li = os.listdir(os.getcwd())#列出目录下的所有文件和目录
    #print 'dirlist:',li
    for i in range(len(li)):
        if  "vote-data"  in li[i]:
            li2.append(li[i])
            print 'li2:',li2
    li2.sort();
    dir = li2[-1]
    print 'dir:',dir

    for i in range(179):
        fname = "list" + str(i + 1) + ".txt"
        f = open(dir + "/" + fname)
        rows = json.load(f)
        for r in rows:
            if nodename in r['producers']:
                # print r["owner"] + "   " + str(r["staked"]) + "  " + r["last_vote_weight"]
                owner = r["owner"]
                stacked = int(r["staked"])
                producers = len(r["producers"])
                l = {}
                l["staked"] = stacked
                l["prod_num"] = producers
                d[owner] = l


    res = sorted(d.items(), key=lambda x: x[1], reverse=True)
    #print 'res:',str(res)
    l = []
    for j in res:
        if int(j[1]["staked"]) > 1000000000:
            #print j[0] + "  " + str(j[1])
            l.append(j)
    return l,len(res)



class TodoHandler(BaseHTTPRequestHandler):
#    A simple TODO server
#    which can display and manage todos for you.

    # Global instance to store todos. You should use a database in reality.
    TODOS = []
    print 'TODOS'
    def do_GET(self):
        # return all todos
        print 'do_GET'

        if self.path != '/':
            self.send_error(404, "File not found.")
            return
        print 'do_GET'
        # Just dump data to json, and return it
        message = json.dumps(self.TODOS)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(message)

    def do_POST(self):
        print 'do_POST'
#        Add a new todo
#        Only json data is supported, otherwise send a 415 response back.
#        Append new todo to class variable, and it will be displayed
#        in following get request
        print 'self:',self.headers
        print '\nself.rfile:',self.rfile
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        print 'pdict:',pdict
        if ctype == 'application/json' or ctype == 'application/x-www-form-urlencoded':
            lent = int(self.headers['content-length'])
            post_values = json.loads(self.rfile.read(lent))
            name = post_values['node']
            print 'name:',name
            data = {}
            data['voters'],data['voter_num'] = search_name(name)
            data['producer_info'] = http_client(name)
            send_values = json.dumps(data)
            print 'send_values:',send_values
            self.TODOS.append(send_values)
            
        else:
            print 'ctype:',ctype
            self.send_error(415, "Only json data is supported.")
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(send_values)

if __name__ == '__main__':
    # Start a simple server, and loop forever
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 8001), TodoHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()


