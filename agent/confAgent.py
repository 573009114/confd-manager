#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,socket
import os,sys

class mysqlClient:
    def __init__(self):
        self.db=MySQLdb.connect("127.0.0.1", "root", "", "confd", charset='utf8' )
        self.cursor = self.db.cursor()
        self.ip = socket.gethostbyname(socket.gethostname())

    def viewSQL(self):
        sql="SELECT keyname FROM omds_keylist WHERE id IN ( SELECT kid_id FROM omds_hostalias WHERE sid_id IN ( SELECT id FROM omds_servers WHERE servearip LIKE '%s' ) );" % self.ip
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        response=[]
        try:
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
            for row in result:
                response.append(row[0])
        except:
            response='异常信息，请检查数据库连接状态'
        self.db.close()
        return response


class templateConf:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.response=mysqlClient().viewSQL()      
            
    def Toml(self):
        for key in self.response:
           keyname=key
           vhosts=key.split('/')[-1]
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
           keyname=key
           vhosts=key.split('/')[-1]

           tmpl='''
{{{{range getvs "{keyname}"}}}}
{{{{.}}}}
{{{{end}}}}
'''.format(keyname=keyname)
           handle = open('/opt/confd/templates/%s.tmpl' % vhosts,'w')
           handle.write(tmpl)
           handle.close()


def main():
    os.system('rm -fr //opt/confd/conf.d/*.toml')
    os.system('rm -fr //opt/confd/templates/*.tmpl')
    templateConf().Toml()
    templateConf().Tmpl()
    os.system('/opt/confd/bin/confd -watch -backend etcd -node=http://127.0.0.1:2379 -confdir /opt/confd/ &')
if __name__ == '__main__':
    main()
