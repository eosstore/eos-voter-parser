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

#获取投票信息的文件夹和文件夹中的文件个数
def getvotefile():
    li = os.listdir(data_dir)#列出目录下的所有文件和目录
    li.sort();
    dir = li[-2]
    #print 'dir:',dir
    file_num = os.listdir(data_dir+'/'+dir)
    #print 'file_num',len(file_num)
    if len(file_num) < 10:
        dir = li[-3]
        print 'dir:',dir
        file_num = os.listdir(data_dir+'/'+dir)
        print 'file_num',len(file_num)
    return file_num,dir


def votes2eos(votes):
     date = (int(time.time()) - (946684800000 / 1000))
     weight = float(date/ (24 * 3600 * 7) )/float( 52 )
     #print 'weight',weight,it['total_votes']
     return (float(votes)/ pow( 2, weight ))/10000
 

 
#voter = {}
def get_voter_info(votername):
    d = {}
#    li2 = []
    #get  vote-data
    #li = os.listdir(os.getcwd())#列出目录下的所有文件和目录
    file_num,dir = getvotefile()
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
    #print 'voter',voter
    pl = voter['producers'] 

    #获取produce信息
    pl2 = []
    bp = http_client("all","get_producers")
    #print 'bp',bp
    for name in pl:
        pd = {}
        total = 0
        pd['producer_name'] = name
        for it in bp:
            if it['owner'] == name:
                pd['total_eos'] = int(votes2eos(it['total_votes']))
                pd['pecent'] = float(it['total_votes'])/float(http_client(name,"get_table_rows"))
        pl2.append(pd) 
    voter['producers'] = pl2
    return voter



def search_name(nodename):
    d = {}
    file_num,dir = getvotefile()
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
                l["time"] = dir[10:]
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
    #cur_d[nodename] = l 
    #print 'cur_d',cur_d
    total = []
    total.append(len(res))
    total.append(total_eos/10000)
    return l,total


pre_d = {} 
#初始化投票列表
def init_votes(number):
    d = {}
    nodename = 'eosstorebest'
    li = os.listdir(data_dir)#列出目录下的所有文件和目录
    li.sort();
    dir = li[number]
    #print 'dir:',dir
    file_li = os.listdir(data_dir+'/'+dir)
    for i in range(len(file_li)):
        fname = "list" + str(i + 1) + ".txt"
        f = open(data_dir + '/'+dir + "/" + fname)
        rows = json.load(f)
        for r in rows:
            if nodename in r['producers']:
                # print r["owner"] + "   " + str(r["staked"]) + "  " + r["last_vote_weight"]
                owner = r["owner"]
                stacked = int(r["staked"])
                if stacked > 1000000000:
                    l = {}
                    l["staked"] = stacked
                    l["status"] = 'voted'
                    l["time"] = dir[10:]
                    d[owner] = l
    #print 'd ----->',d

    dit = {}
    dit[nodename] = d
    return dit

#比较两次的投票信息的差别
def get_compare(nodename):
    cur_d = {}
    cur_d = init_votes(-2)
    d1 = pre_d[nodename]
    d2 = cur_d[nodename]
    print 'd1:',d1
    print 'd2:',d2
    
    #for i in d2:
    #    print 'i--->',i
    #    if d1.has_key(i):
    #        print 'voted 1'
    #        d1[i]["status"] = 'voted'
    #    else:
    #        print 'added:',i
    #        n = {}
    #        d2[i]["status"] = 'added'
    #        n[i] = d2[i]
    #        d1.update(n)
    for i in d1:
        if d2.has_key(i):
            print 'voted 2'
            #d1[i]["status"] = 'voted'
        else:
            print 'deleted :',i
            d1[i]["status"] = 'deleted'
    return d1

# ------------------------------------------------------------------------------------------
# ------ Goto http handler
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
            data['producer_info'] = http_client(name,"get_producers")
            #print 'producer_ifno',data['producer_info']
            data['total_eos'] = int(votes2eos(data['producer_info']['total_votes']))
            data['percent'] = float(data['producer_info']['total_votes'])/float(http_client(name,"get_table_rows"))
        elif post_values.has_key('voter'):
            name = post_values['voter']
            data = get_voter_info(name)
        elif post_values.has_key('compare'):
            name = post_values['compare']
            data = get_compare(name)
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
    pre_d = init_votes(1)
    app = make_app()
    print 'service is start.'
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8002)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
