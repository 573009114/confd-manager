## 部署教程
# 欢迎大家指正，我也会随时提交，并迭代。 感谢！


#### 逻辑架构图 
![image](https://github.com/573009114/confd-manager/blob/master/pic/jiagoutu.jpg)

#### 1、安装python2.7
```
安装方式略。可以选择centos7.x版本


安装mariadb mariadb-server mariadb-devel

安装python-devel ,python-etcd

安装Cython，

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
注： 可以将agent 里面的数据库地址修改，并放到对应安装了confd和nginx的服务器，执行即可，会自动启动confd和生成模板。
```
##### 启动 （可选项） 
```
启动 confd 并从etcd里面读取信息
/opt/confd/bin/confd -watch -backend etcd -node=http://127.0.0.1:2379 -confdir /opt/confd/
```

#### 4、部署代码
```
git clone https://github.com/573009114/confd-manager.git
```
#### 5、修改setting.py配置
```
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'confd',
         'USER':'confduser',
         'PASSWORD':'confd123',
         'HOST':'127.0.0.1',
         'PORT':'3306',
     }
}

```

#### 6、效果展示
![image](https://github.com/573009114/confd-manager/blob/master/pic/index.jpg)
![image](https://github.com/573009114/confd-manager/blob/master/pic/zhanshi.jpg)


#### 7、客户端安装
```
客户端安装：
yum install epel-release -y
yum install MySQL-python -y
运行confdAgent
```
 
