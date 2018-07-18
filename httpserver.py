# -*- coding: UTF-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
import re
import sys
import os
import requests
import time

import tornado.ioloop
import tornado.web
import tornado.httpserver

data_dir = '/root/voters'
#data_dir = '/root/eos-voter-parser'

def http_client(nodename,option):
    #url = 'https://vote.changshang15.com/v1/chain/get_producers'
    # url curl --request POST --url https://vote.changshang15.com/v1/chain/get_producers --data '{"limit":"100","json":"true"}'
    url = 'http://127.0.0.1:8889/v1/chain/'

    url = url + option
    # Make a POST request and read the response
    headers = {'content-type': 'application/json'}
    if option == "get_producers":
        data = json.dumps({"limit":"230","json":"true"})
        res = requests.post(url, data=data, headers=headers)
        res = json.loads(res.text)
        if nodename == "all":
            return res['rows']
        else:
            for it in iter(res['rows']):
                if it['owner'] == nodename:
                    #print it
                    return it
    elif option == "get_table_rows":
        data = json.dumps({"scope":"eosio","code":"eosio","table":"global","json":"true"})
        res = requests.post(url, data=data, headers=headers)
        res = json.loads(res.text)
        #total_stake = res['total_ram_stake']
        row = res['rows']
        if len(row) > 0:
            #print row[0]
            return row[0]['total_producer_vote_weight']
    #print(res.text)
 
voter = {}
def get_voter_info(votername):
    d = {}
#    li2 = []
    #get  vote-data
    #li = os.listdir(os.getcwd())#列出目录下的所有文件和目录
    li = os.listdir(data_dir)#列出目录下的所有文件和目录
    li.sort();
    dir = li[-2]
    print 'dir:',dir
    file_num = os.listdir(data_dir+'/'+dir)
    print 'file_num',len(file_num)
    if len(file_num) < 140:
        dir = li[-3]
        print 'dir:',dir
        file_num = os.listdir(data_dir+'/'+dir)
        print 'file_num',len(file_num)
    voter = {}
    #获取voter信息
    for i in range(len(file_num)):
        fname = "list" + str(i + 1) + ".txt"
        f = open(data_dir+'/'+dir + "/" + fname)
        rows = json.load(f)
        for r in rows:
            if r["owner"] == votername:
                voter = r
                break
        if len(voter) > 0:
            break
    print 'voter',voter
    pl = voter['producers'] 

    #获取produce信息
    pl2 = []
    bp = http_client("all","get_producers")
    print 'bp',bp
    for name in pl:
        pd = {}
        total = 0
        pd['producer_name'] = name
        #for i in range(len(file_num)):
        #    fname = "list" + str(i + 1) + ".txt"
        #    f = open('/root/eos-voter-parser/'+dir + "/" + fname)
        #    rows = json.load(f)
        #    for r in rows:
        #        if name in r['producers']:
        #            total += int(r["staked"])            
        #pd['total_eos'] = total/10000
        #print 'staked',staked
        for it in bp:
            if it['owner'] == name:
                date = (int(time.time()) - (946684800000 / 1000))
                weight = float(date/ (24 * 3600 * 7) )/float( 52 )
                #print 'weight',weight,it['total_votes']
                pd['total_eos'] = (float(it['total_votes'])/ pow( 2, weight ))/10000
                pd['pecent'] = float(it['total_votes'])/float(http_client(name,"get_table_rows"))
        pl2.append(pd) 
    voter['producers'] = pl2
    return voter
    

def search_name(nodename):
    d = {}
#    li2 = []
    #get  vote-data
    #li = os.listdir(os.getcwd())#列出目录下的所有文件和目录
    li = os.listdir(data_dir)#列出目录下的所有文件和目录
    li.sort();
    dir = li[-2]
    print 'dir:',dir
    file_num = os.listdir(data_dir+'/'+dir)
    print 'file_num',len(file_num)
    for i in range(len(file_num)):
        fname = "list" + str(i + 1) + ".txt"
        f = open(data_dir + '/'+dir + "/" + fname)
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
    total_eos = 0
    for j in res:
        global total_eos
        total_eos += j[1]["staked"]
        if int(j[1]["staked"]) > 1000000000:
            #print j[0] + "  " + str(j[1])
            l.append(j)
    total = []
    total.append(len(res))
    total.append(total_eos/10000)
    return l,total

# ------------------------------------------------------------------------------------------
# ------ Create Account Handler
# ------------------------------------------------------------------------------------------

class GotoHttpHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)

    def _handle(self, request):
        print 'request.body:',request.body
        post_values = json.loads(request.body.decode())
        data = {}
        if post_values.has_key('node'):
            name = post_values['node']
            print 'name:',name
            data['voters'],total = search_name(name)
            data['voter_num'] = total[0]
            data['total_eos'] = total[1]
            data['producer_info'] = http_client(name,"get_producers")
            data['percent'] = float(data['producer_info']['total_votes'])/float(http_client(name,"get_table_rows"))
        elif post_values.has_key('voter'):
            name = post_values['voter']
            data = get_voter_info(name)
        send_values = json.dumps(data)
        print 'send_values:',send_values

        #self.write(json.dumps(send_values))
        self.write(send_values)
        #else:
     #   failmsg = "{\"msg\":\"failed, failed to generate keys\"}"
      #  self._write_response(400, failmsg)



    def post(self):
        print 'post=='
        self._handle(self.request)

    #def get(self):
    #    self._handle(self.request)



def make_app():
  return tornado.web.Application([
    (r"/", GotoHttpHandler),
  ])


if __name__ == '__main__':
    # Start a simple server, and loop forever
    app = make_app()
    print 'service is start.'
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8001)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
