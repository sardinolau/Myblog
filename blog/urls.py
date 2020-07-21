from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path("backend/add_article/",views.add_article),
    path(r"up_down/",views.up_down),
    re_path(r"comment/",views.comment),

    re_path(r"comment_tree/(\d+)/",views.comment_tree),

    #三合一URL
    # re_path(r'(\w+)/(tag|category|archive)/(.+)',views.home),
    re_path(r'(\w+)/article/(\d+)/$',views.article_detail),
    re_path(r'(?P<username>\w+)',views.home),#相当于传送了一个关键字参数
]