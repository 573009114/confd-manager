#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,socket
import os,sys

class mysqlClient:
    def __init__(self):
        self.db=MySQLdb.connect("127.0.0.1", "root", "", "confd", charset='utf8' )
        self.cursor = self.db.cursor()

    def viewSQL(self):
        sql='select keyname from omds_projectList;'
        keyname=[]
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for row in result:
                keyname.append(row[0])
            return keyname
        except:
            msg='异常信息，请检查数据库连接状态'
            return msg
        self.db.close()


class templateConf:
    def __init__(self):
        self.ipaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        self.response=mysqlClient().viewSQL()

    def Toml(self):
        for key in self.response:
            if self.ipaddr in key:
                keyname=key
                vhosts=key.split('/')[5]
                toml='''
[template]
src = "{vhosts}.tmpl"
dest = "/opt/openresty/nginx/conf/vhost/{vhosts}.conf"
keys =[
      "{keyname}",
]

check_cmd = "/opt/openresty/nginx/sbin/nginx -t"
reload_cmd = "/opt/openresty/nginx/sbin/nginx -s reload"
'''.format(vhosts=vhosts,keyname=keyname)    
                handle = open('/opt/confd/conf.d/%s.toml' % vhosts,'w')
                handle.write(toml)
                handle.close()

    def Tmpl(self):
        for key in self.response:
            if self.ipaddr in key:
                keyname=key
                vhosts=key.split('/')[5]

                tmpl='''
{{{{range getvs "{keyname}"}}}}
{{{{.}}}}
{{{{end}}}}
'''.format(keyname=keyname)
                handle = open('/opt/confd/templates/%s.tmpl' % vhosts,'w')
                handle.write(tmpl)
                handle.close()







def main():
    templateConf().Toml()
    templateConf().Tmpl()
    os.system('/opt/confd/bin/confd -watch -backend etcd -node=http://127.0.0.1:2379 -confdir /opt/confd/ &')
if __name__ == '__main__':
    main()
