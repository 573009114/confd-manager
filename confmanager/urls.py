"""confweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from confmanager import project,views,account,group,server

urlpatterns = [
#    url(r'^$',views.dashboard,name='dashboard'),
    url(r'^$',views.dashboard,name='dashboard'),
    url(r'^login/$',account.login,name='login'),
    url(r'^logout/$',account.logout,name='logout'),
    url(r'^channgepwd/$',account.channgePwd,name='channgepwd'),
    url(r'^config/project/$',project.viewConfig),
    url(r'^config/project/del',project.projectDel,name='del'),
    url(r'^config/project/add',project.projectAdd,name='add'),
    url(r'^config/project/edit',project.projectEdit,name='edit'),
    url(r'^config/project/channge',project.projectChannge,name='channge'),
    url(r'^config/project/rollback',project.projectRollback,name='rollback'),
    url(r'^config/project/push',project.confPush,name='push'),
    url(r'^config/server/$',server.serverList,name='serverlist'),
    url(r'^config/server/add',server.serverAdd,name='serveradd'),
    url(r'^config/server/del',server.serverDel,name='serverdel'),
    url(r'^config/group/$',group.groupList,name='grouplist'),
    url(r'^config/group/add',group.addGroup,name='groupadd'),
    url(r'^config/group/del',group.delGroup,name='groupdel'),
    url(r'^config/group/push',group.pushGroupKey,name='pushgroup'),
    url(r'^config/group/setgroupconfig',group.setGroupConfig,name='setgroupconfig'),
]
