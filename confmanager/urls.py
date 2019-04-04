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
from confmanager import index,views,account

urlpatterns = [
    url(r'^$',views.dashboard,name='dashboard'),
    url(r'^login/$',account.login,name='login'),
    url(r'^logout/$',account.logout,name='logout'),
    url(r'^channgepwd/$',account.channgePwd,name='channgepwd'),
    url(r'^config/project/$',index.viewConfig),
    url(r'^config/project/del',index.projectDel,name='del'),
    url(r'^config/project/add',index.projectAdd,name='add'),
    url(r'^config/project/edit',index.projectEdit,name='edit'),
    url(r'^config/project/channge',index.projectChannge,name='channge'),
    url(r'^config/project/rollback',index.projectRollback,name='rollback'),
    url(r'^config/project/push',index.confPush,name='push'),
    url(r'^config/server/$',index.serverList,name='serverlist'),
    url(r'^config/server/add',index.serverAdd,name='serveradd'),
    url(r'^config/server/del',index.serverDel,name='serverdel'),
]
