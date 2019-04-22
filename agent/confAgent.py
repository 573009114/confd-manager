#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,socket
import os,sys
import urllib
import urllib2
import shutil
import commands
import subprocess


class mysqlClient(object):
    def __init__(self):
        self.db=MySQLdb.connect("10.52.15.200", "confd", "confdmanager", "confdweb", charset='utf8' )
        self.cursor = self.db.cursor()
    def viewSQL(self,sql):
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        response=[]
        try:
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
            for row in result:
                response.append(row)
        except:
            response='异常信息，请检查数据库连接状态'
        self.db.close()
        return response

class ngxTemp(object):
    def __init__(self,sql):
      self.key = mysqlClient().viewSQL(sql)
    def ngxConftoml(self):
        for ngxName in self.key:
            ngxkeyName=ngxName[0]
            ngxkeyfiles=ngxName[0].split('/')[2]+'_conf'

            _ngxConftoml='''
                [template]
                src = "{ngxkeyfiles}.tmpl"
                dest = "/opt/openresty/nginx/conf/nginx.conf"
                keys =[
                      "{ngxkeyName}",
                ]

                check_cmd = "/opt/openresty/nginx/sbin/nginx -t"
                reload_cmd = "/opt/openresty/nginx/sbin/nginx -s reload"
                '''.format(ngxkeyName=ngxkeyName,ngxkeyfiles=ngxkeyfiles)
            handle = open('/opt/confd/conf.d/%s.toml' % ngxkeyfiles,'w')
            handle.write(_ngxConftoml)
            handle.close()

    def ngxConftmpl(self):
        for ngxName in self.key:
            ngxkeyName=ngxName[0]
            ngxkeyfiles=ngxName[0].split('/')[2]+'_conf'

            _nginxConftmpl='''
              {{{{range getvs "{ngxkeyName}"}}}}
              {{{{.}}}}
              {{{{end}}}}
              '''.format(ngxkeyName=ngxkeyName)
            handle = open('/opt/confd/templates/%s.tmpl' % ngxkeyfiles,'w')
            handle.write(_nginxConftmpl)
            handle.close()



class template(object):
    def __init__(self,sql):
        self.key=mysqlClient().viewSQL(sql)
        vhost=[]
        rewrite=[]
        for i in self.key:
            vhost.append(i[0])
            rewrite.append(i[1])
        self.vhost=vhost
        self.rewrite=rewrite



# 生成vhost toml文件    
    def vhostToml(self): 
        for key in self.vhost:
            keyhostName=key.split('/')[4]+'_vhost'
        
            _vhosttoml='''
                 [template]
                 src = "{keyhostName}.tmpl"
                 dest = "/opt/openresty/nginx/conf/vhost/{keyhostName}.conf"
                 keys =[
                      "{key}",
                  ]

                 check_cmd = "/opt/openresty/nginx/sbin/nginx -t"
                 reload_cmd = "/opt/openresty/nginx/sbin/nginx -s reload"
                 '''.format(keyhostName=keyhostName,key=key)
            handle = open('/opt/confd/conf.d/%s.toml' % keyhostName,'w')
            handle.write(_vhosttoml)
            handle.close()

    # 生成rewrite toml文件
    def rewriteToml(self):
        for rewrite in self.rewrite:
            keywriteName=rewrite.split('/')[4]+'_rewrite'
            _rewritetoml='''
            [template]
            src = "{keywriteName}.tmpl"
            dest = "/opt/openresty/nginx/conf/rewrite/{keywriteName}.conf"
            keys =[
                "{rewrite}",
              ]

            check_cmd = "/opt/openresty/nginx/sbin/nginx -t"
            reload_cmd = "/opt/openresty/nginx/sbin/nginx -s reload"
            '''.format(keywriteName=keywriteName,rewrite=rewrite)
            handle = open('/opt/confd/conf.d/%s.toml' % keywriteName,'w')
            handle.write(_rewritetoml)
            handle.close()
        return bool(True)

    # 生成vhost 模板文件
    def vhostTmpl(self):
        for key in self.vhost:
            keyname=key.split('/')[4]+'_vhost'
            _vhosttmpl='''
              {{{{range getvs "{key}"}}}}
              {{{{.}}}}
              {{{{end}}}}
              '''.format(key=key)
            handle = open('/opt/confd/templates/%s.tmpl' % keyname,'w')
            handle.write(_vhosttmpl)
            handle.close()

    # rewrite 模板文件
    def rewriteTmpl(self):
        for rewrite in self.rewrite:
            keyrewriteName=rewrite.split('/')[4]+'_rewrite'
            _vrewritetmpl='''
              {{{{range getvs "{rewrite}"}}}}
              {{{{.}}}}
              {{{{end}}}}
              '''.format(rewrite=rewrite)
            handle = open('/opt/confd/templates/%s.tmpl' % keyrewriteName,'w')
            handle.write(_vrewritetmpl)
            handle.close()
    
class initConfd(object):
    def __init__(self):

        skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        skt.connect(('8.8.8.8',80))
        socketIpPort = skt.getsockname()
        self.ip = socketIpPort[0]



        os.system('mkdir -p /opt/confd/{conf.d,bin,templates}/ && rm -fr /opt/confd/conf.d/*.toml && rm -fr /opt/confd/templates/*.tmpl')
        url='https://github.com/kelseyhightower/confd/releases/download/v0.16.0/confd-0.16.0-linux-amd64'
        if os.path.isfile('/opt/confd/bin/confd'):
            os.system('chmod +x /opt/confd/bin/confd')
            print 'confd file is exist...'
        else:
            print 'Files are being downloaded...'
            urllib.urlretrieve(url, "confd-0.16.0-linux-amd64")
            shutil.move('confd-0.16.0-linux-amd64','/opt/confd/bin/confd')
            os.system('chmod +x /opt/confd/bin/confd')
            print 'confd file download completed!!!'

    def startconfd(self):
        sql1="SELECT keyhost,keyrewrite FROM omds_servers c LEFT JOIN omds_hostalias a ON a.sid_id = c.id LEFT JOIN omds_keylist b ON a.kid_id = b.id WHERE servearip = '%s'; " % self.ip
        sql2="SELECT keyngx FROM omds_groups where id in (SELECT group_id FROM  omds_servers WHERE servearip='%s'); " % self.ip
        template(sql1).rewriteToml()
        template(sql1).vhostToml()
        template(sql1).rewriteTmpl()
        template(sql1).vhostTmpl()
        ngxTemp(sql2).ngxConftoml()
        ngxTemp(sql2).ngxConftmpl()
        os.popen('/opt/confd/bin/confd -watch -backend etcd -node=http://10.52.15.200:2379 -confdir /opt/confd/')


if __name__ == '__main__':
    try:
        arg=sys.argv[1]
        if arg == 'version':
            print 'version: v1.1.1'
    except:
        initConfd().startconfd()

