# eos-voter-parser

第一步：生成数据库中的voters信息
```
$./parser.sh 
```
这里有两个服务端程序，server.py是用request实现，未实现多并发；httpserver.py是利用tornado实现多并发服务，访问要比前面的速度快。

第二步：启动服务
```
$python httpserver.py
```
第三部：访问接口
```
$curl --request POST   --url http://172.0.0.1:8001   --data '{"node":"<bpaccountname>"}'
$curl --request POST   --url http://172.0.0.1:8001   --data '{"voter":"<account>"}'
```
说明：

1.如果需要定时执行parser.sh，需要利用Linux的crontab；

   crontab -e 编辑   cronatab -l 查看（详细可以自行查阅crontab相关文档）
   
   */15 * * * * /root/eos-voter-parser/./parser.sh  1>>/root/voters/voters.log 2>&1
   
   启动cron start
   
2.如果需要httpserver一直运行，可以使用systemctl 启动，详细配置请自行查阅相关文档

