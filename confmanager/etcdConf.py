#_*_ coding:utf-8 _*_

import etcd

class etcdClient:
    def __init__(self):
        self.client=etcd.Client(host='127.0.0.1', port=4001)

    def viewValue(self,keyName):
        try:
            result=self.client.read('%s' % keyName).value
            return result
        except etcd.EtcdKeyNotFound:
            result='Etcd key is not found ...'

    def writeValue(self,keyName,Value):
       result=self.client.write('%s' % keyName,'%s' % Value).value
       return result

    def delKey(self,keyName):
        result=self.client.delete('%s' % keyName)

        return result


 
