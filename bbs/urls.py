"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from blog import views
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('reg/', views.register),
    path('index/', views.index),
    #将所有以blog开头的，都交给blog里的url来处理
    path('blog/', include("blog.urls")),
    path('get_valid_img/', views.get_valid_img),
    # path('reg/', views.reg),
    #极验滑动验证码，获取验证码的url
    path('pc-geetest/register', views.get_geetest),
    #用来校验用户名是否被注册
    path('check_username_exist/', views.check_username_exist),
    #设置media的路由
    re_path("media/(?P<path>.*)$",serve,{"document_root": settings.MEDIA_ROOT}),

    path('upload/', views.upload),

]
