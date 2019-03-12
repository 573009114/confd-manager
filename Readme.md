## 部署教程


#### 架构图  （ps:图是盗的，拿来占个未知，思路和这个图类似。）
![image](https://images2015.cnblogs.com/blog/305504/201611/305504-20161128231227318-454123414.png)

#### 1、安装python2.7
```
安装方式略。可以选择centos7.x版本

安装mariadb mariadb-server mariadb-devel

安装MySQL-python.x86_64 模块
```

#### 2、部署etcd 这里是单机版本 （高可用方案也简单，可以参考我的其他github文档。）
```
yum install etcd -y 
```
```
配置信息 参考

[Member]
ETCD_NAME=confd-etcd
ETCD_DATA_DIR="/export/etcd/"
ETCD_LISTEN_PEER_URLS="http://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379,http://0.0.0.0:4001"
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://127.0.0.1:2380"
ETCD_INITIAL_CLUSTER="confd-etcd=http://127.0.0.1:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_ADVERTISE_CLIENT_URLS="http://127.0.0.1:2379,http://127.0.0.1:4001"
ETCD_DISCOVERY=""

```

#### 3、部署confd
```
wget https://github.com/kelseyhightower/confd/releases/download/v0.16.0/confd-0.16.0-linux-amd64
mkdir -p /opt/confd/bin
mv confd-0.16.0-linux-amd64 /opt/confd/bin/confd
chmod +x /opt/confd/bin/confd
export PATH="$PATH:/opt/confd/bin"
```
 
##### 3.1 创建配置文件
###### nginx.toml
```
[template]
src = "nginx.conf.tmpl"
dest = "/opt/openresty/nginx/conf/vhost/test.conf"

keys =[
      "/test/nginx",
]

check_cmd = "/opt/openresty/nginx/sbin/nginx -t"
reload_cmd = "/opt/openresty/nginx/sbin/nginx -s reload"

```
###### nginx.conf.tmpl
```
{{range getvs "/test/nginx/*"}}
  {{.}}
{{end}}

```

 
```
启动 confd 并从etcd里面读取信息
/opt/confd/bin/confd -watch -backend etcd -node=http://127.0.0.1:2379 -confdir /opt/confd/
```

#### 4、部署代码

#### 5、修改setting.py配置
