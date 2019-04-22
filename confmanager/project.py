# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
from viewConf import *
from etcdConf import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json,etcd
import datetime

def global_env():
    Version=datetime.datetime.now().strftime("v%Y%m%d%H%M%S")
    return Version

########################################################
@login_required
def viewConfig(req):
    if req.method == 'GET':
        typed=req.GET.get('typed')
        id=req.GET.get('id')
      
        if typed == 'product':
            response=viewsConf(typed).envConf()
      
            env={'name':'线上环境'}
        elif typed == 'develop':
            response=viewsConf(typed).envConf()
       
            env={'name':'研发环境'}
        elif typed == 'test':
            response=viewsConf(typed).envConf()
      
            env={'name':'测试环境'}
        else:
            response=viewsConf(typed).envAll()
            env={'name':'所有环境'}
        return render(req,'project-type.html',{'response':response,'env':env})

# 编辑配置
@login_required
def projectChannge(req):
    id=req.GET.get('pid')
    serverlist=viewsServer()
    env={'name':'编辑配置','version':global_env(),'typed':'详情'}
    if req.method == 'GET':
        defaultContent=projectConf(pid=id).defaultProJectConf()
        response={'DEFAULT':defaultContent}
    elif req.method == 'POST':
        confContent=req.POST.get('configText')
        rewrite=req.POST.get('rewrite')
        creatVersion=projectConf(pid=id,version=global_env(),confContent=confContent,rewrite=rewrite).CreateVersion()
        return HttpResponse('<script type="text/javascript">alert("配置修改完成");location.href="javascript:history.back(-1);"</script>')
    return render(req,'project-content.html',{'response':response,'env':env,'serverlist':serverlist})

# 推送配置到etcd
@login_required
def confPush(req):
    id=req.GET.get('pid')
    response=projectConf(pid=id).findProjectConf()

    keyName=response['keyName']
    keyrewrite=response['keyrewrite']
    try:
        vhost=projectConf(pid=id).defaultProJectConf()[0]['confText']
        rewrite=projectConf(pid=id).defaultProJectConf()[0]['rewrite']
        if rewrite =='':
            etcdClient().writeValue(keyName,vhost)
            msg="推送成功，注意:rewrite内容为空"
        else:
            etcdClient().writeValue(keyName,vhost)
            etcdClient().writeValue(keyrewrite,rewrite)
            msg="推送完成"
    except TypeError:
        msg='推送数据为空,请检查配置内容'
    except UnicodeEncodeError:
        msg='编码错误，配置文件中包含异常字符。'
#    except:
#        msg='etcd推送失败，请检查服务或者逻辑是否正常'
    return HttpResponse('<script type="text/javascript">alert("%s");location.href="javascript:history.back(-1);"</script>'% msg)

# 项目新增
@login_required
def projectAdd(req):
    env='新增项目'

    response={
        'groups':viewGroup(),
        'servers':viewsServer()
    }

    if req.method == 'POST':
        typed=req.POST.get('type')
        env_type=req.POST.get('envtype')
        projectName=req.POST.get('projectname')
        serverName=req.POST.get('servername')
        vhost=req.POST.get('domain')
        cluster=req.POST.get('cluster')
        groupid=req.POST.get('groupid')
      
       
        keyname=('/%s/%s/%s/%s/vhost' %(env_type,serverName,cluster,vhost))
        keyrewrite=('/%s/%s/%s/%s/rewrite' %(env_type,serverName,cluster,vhost))
        keyngx=('/%s/%s/%s/%s/nginx' %(env_type,serverName,cluster,vhost))


        sid=projectConf(groupid=groupid).findServer()
        _sid=[]
        for s in sid:
            _sid.append(s['id'])

        kid=projectConf(typed=typed,env_type=env_type,
            projectName=projectName,serverName=serverName,
            vhost=vhost,keyname=keyname,keyrewrite=keyrewrite,groupid=groupid).addProJectConf()   
        if kid is not False:
            if len(sid) != 0:
                # 关联keyid与serverid
                addHostid(_sid,kid)
                response=HttpResponse('<script type="text/javascript">alert("项目添加完成");location.href="/config/project/add"</script>')
            else:
                response=HttpResponse('<script type="text/javascript">alert("警告：IP未关联,项目添加成功");location.href="/config/project/add"</script>')
        else:
            response=HttpResponse('<script type="text/javascript">alert("错误：重复添加");location.href="/config/project/add"</script>')
        return response
    return render(req,'project-add.html',{'env':env,'response':response})

# 项目关联
@login_required
def projectEdit(req):
    kid=req.GET.get('pid')
    serverlist=viewsServer()
    response=EditConf(pid=kid).projectconfig()
    joinip=selectSid(pid=kid)
    env={'name':'项目关联','version':global_env()}
    if req.method =='POST': 
        sid=req.POST.getlist('sid[]')
        updateHostid(sid,kid)
        return HttpResponse('<script type="text/javascript">alert("IP关联更新成功");location.href="javascript:history.back(-1);"</script>')
    return render(req,'project-edit.html',{'response':response,'serverlist':serverlist,'env':env,'joinip':joinip})


# 项目删除
@login_required
def projectDel(req):
    id=req.GET.get('pid')
    obtainKey=projectConf(pid=id).findProjectConf()
    try:
        keyName=obtainKey['keyName']
        keyrewrite=obtainKey['keyrewrite']

        delEtcd=etcdClient().delKey(keyName)
        delEtcd=etcdClient().delKey(keyrewrite)    #推送到etcd
        response=projectConf(pid=id).delProJectConf()
    except:
        response=projectConf(pid=id).delProJectConf()
    return HttpResponse('<script type="text/javascript">alert("记录删除");location.href="/config/project/"</script>')

# 项目配置回滚
@login_required
def projectRollback(req):
    historyVersions=req.GET.get('versions')
    env={'name':'项目回滚编辑'}
    config=projectConf(version=historyVersions).rollback()
    pid=config[0]['kid_id'] 

    if req.method == 'GET':  
        domain=projectConf(pid=pid).defaultProJectConf()   
        response={'VERSION':domain,'DEFAULT':config}
        return render(req,'project-rollback.html',{'response':response,'env':env})
    elif req.method == 'POST':
        confContent=req.POST.get('configText')
        rewrite=req.POST.get('rewrite')
        response=projectConf(pid=pid,version=global_env(),confContent=confContent,rewrite=rewrite).CreateVersion()
        return HttpResponse('<script type="text/javascript">alert("配置回滚完成，并生成新的版本号");location.href="/config/project/"</script>')
