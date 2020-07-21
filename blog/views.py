

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse,response
from django.contrib import auth
from geetest import GeetestLib
from django.db.models import Count
from bs4 import BeautifulSoup
import json

from blog import forms
from blog import models
import logging.config


# Create your views here.
#使用验证登录码的登录
# def login(request):
#     #if request is ajax  #如果是ajax请求
#     # if request.method =="POST":
#     if request.is_ajax():
#         #初始化一个给AJAX返回的数据 Ajax请求返回一个字典
#         ret = {"status": 0,"msg":""}
#         #从提交过来的数中 取到用户名和密码
#
#         username = request.POST.get('username')
#         pwd = request.POST.get("password")
#         valid_code = request.POST.get('valid_code')  #获取用户填写的验证码
#         print(valid_code)
#         print('用户输入的验证码'.center(120,"="))
#         if valid_code and valid_code.upper() == request.session.get("valid_code","").upper():
#             user_obj = auth.authenticate(username=username,password = pwd)
#             if user_obj:
#                 ret['status']=user_obj
#             else:
#                 ret['msg'] = "用户名或密码错误！"
#
#         else:
#             ret['msg'] = "验证码错误"
#         return JsonResponse(ret)
#     else:
#         return render(request, "login.html")

#使用极验验证码的登录
def login(request):
    #if request is ajax  #如果是ajax请求
    # if request.method =="POST":
    if request.is_ajax():
        #初始化一个给AJAX返回的数据 Ajax请求返回一个字典
        ret = {"status": 0,"msg":""}
        #从提交过来的数中 取到用户名和密码

        username = request.POST.get('username')
        pwd = request.POST.get("password")

        #获取极验验证码验证的相关参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            user = auth.authenticate(username=username,password = pwd)

            if user:
                auth.login(request,user)  #将user赋值给request
                ret['status']=username
                ret['msg']="/index/"
            else:
                ret['msg'] = "用户名或密码错误！"

        else:
            ret['msg'] = "验证码错误"
        return JsonResponse(ret)
    else:
        return render(request, "login2.html")

#用户注销
def logout(request):
    auth.logout(request)
    return redirect("/index/")

#获取验证码图片
def get_valid_img(request):
    #方式1 ：读指定图片
    # with open('static/img/valid.jpg',"rb") as f:
    #     data = f.read()
    #方式2：基于PIL模块创建验证码
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO  #实现对内存的控制

    def get_random_color():
        import random
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    img = Image.new("RGB",(350,38),get_random_color())
    # f = open("valid.png","wb")
    # img.save(f,"png")
    # with open('valid.png', "rb") as f:
    #     data = f.read()
    # 方式3：
    # img = Image.new("RGB", (350, 38), get_random_color())
    # f = BytesIO()   #在内存生成了句柄
    # img.save(f,'png')
    # data = f.getvalue()
    #方式4：
    # img = Image.new("RGB", (350, 38), get_random_color())
    # draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype("static/font/maobi.ttf",32)
    # draw.text((50,0),"welcome!",get_random_color(),font=font)
    # f = BytesIO()   #在内存生成了句柄
    # img.save(f,'png')
    # data = f.getvalue()
    #方式5
    img = Image.new("RGB", (350, 38), get_random_color()) #设置图片类型，大小
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/maobi.ttf", 32)
    keep_chr=""
    import random
    for i in range(6):
        random_num = str(random.randint(0,9))
        random_lowalf = chr(random.randint(97,122))
        random_upperalf = chr(random.randint(65,90))
        random_chr = random.choice([random_num,random_lowalf,random_upperalf])

        draw.text((i*30+20, 0), random_chr, get_random_color(), font=font)
        keep_chr += random_chr
    print(keep_chr)
    f = BytesIO()  # 在内存生成了句柄
    img.save(f, 'png')
    data = f.getvalue()
    request.session['valid_code']=keep_chr
    return HttpResponse(data)

def index(request):
    # 查询所有的文章列表
    article_list = models.Article.objects.all()
    print(article_list)
    return render(request,"index.html",{"article_list":article_list})


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
# 处理获取极验验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

#注册的视图函数
def register(request):
    if request.method =="POST":
        ret = {"status":0,"msg":""}
        form_obj = forms.RegForm(request.POST)
        #帮我做校验
        if form_obj.is_valid():

            #校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(avatar = avatar_img,**form_obj.cleaned_data)
            ret["msg"]="/index/"
            return JsonResponse(ret)
            #校验不通过
        else:
            print(form_obj.errors)
            ret["status"] = 1  #进入错误的条件语句
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)
    #生成一个form对象
    form_obj = forms.RegForm()
    return render(request,"register.html",{"form_obj":form_obj})

def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        # 表示用户已经注册
        ret["status"] = 1
        ret["msg"] = "用户名已经被注册！"
    return JsonResponse(ret)

#个人博客页
def home(request,username):
    print(username)
    #去UserInfo表里把用户对象取出来
    user = models.UserInfo.objects.filter(username = username).first()
    print(user)
    if not user:
        return HttpResponse("404")
    #如果用户存在需要将它的所有文章找出来
    blog = user.blog
    #个人的article-list
    article_list = models.Article.objects.filter(user=user)
    #我的文章分类及每个分类下文章数
    #将我的文章按照我的分类分组，并统计出每个分类下面的文章数
    # Category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title","c")
    # #统计当前站点下有哪一些标签，并且安标签统计出文章数
    # tag_list = models.Tag.objects.filter(blog = blog).annotate(c=Count("article")).values("title","c")
    # #把文章按照创建时间进行分类
    # archive_list = models.Article.objects.filter(user=user).extra(
    #     select = {"archive_ym":"date_format(create_time,'%%Y-%%m')"}
    # ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym","c")

    return render(request,"home2.html",{
        "username": username,
        "blog":blog,
        "article_list":article_list,
        # "Category_list":Category_list,
        # "tag_list":tag_list,
        # "archive_list":archive_list,
    })

def article_detail(request,username,pk):
    # pk 访问文章的主键值
    # username 被访问用户的用户名
    user = models.UserInfo.objects.filter(username = username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    article_obj = models.Article.objects.filter(pk = pk).first()

    #所有评论列表
    comment_list = models.Comment.objects.filter(article_id=pk)
    print(comment_list)
    return render(request,"article_detail.html",{
        "username":username,
        "article":article_obj,
        "blog":blog,
        "comment_list":comment_list,
    })

from django.db.models import F
#用户点赞
def up_down(request):
    print(request.POST)
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    user = request.user
    response = {"state": True}
    try:
        models.ArticleUpDown.objects.create(user=user,article_id=article_id,is_up=is_up) #使用点赞和文章的联合唯一进行验证
        models.Article.objects.filter(pk = article_id).update(up_count = F("up_count")+1)
    except Exception as e:
        response = {"state": False}
        response["first_action"] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up

    return JsonResponse(response)

#用户评论
def comment(request):
    response={}
    pid = request.POST.get('pid')
    article_id = request.POST.get('article_id')
    content = request.POST.get('content')
    user_pk = request.user.pk
    if not pid:
        comment_obj = models.Comment.objects.create(article_id=article_id,content=content,user_id=user_pk)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id,content=content,user_id=user_pk,parent_comment_id=pid)

    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d")
    response["content"] = comment_obj.content
    response["username"] = comment_obj.user.username

    return JsonResponse(response)

#评论树
def comment_tree(request,article_id):
    ret = list(models.Comment.objects.filter(article_id=article_id).values("pk","parent_comment_id","content"))
    print(ret)
    return JsonResponse(ret,safe=False)


#新增文章

def add_article(request):
    if request.method == "POST":

        title=request.POST.get("title")
        article_content=request.POST.get("article_content")
        if title and article_content:
            soup = BeautifulSoup(article_content,"html.parser")
            #过滤
            for tag in soup.find_all():
                if tag.name =="script":
                    tag.decompose()

            article_obj = models.Article.objects.create(title=title,user=request.user,desc=soup.text[0:150])
            models.ArticleDetail.objects.create(content=soup.prettify(),article=article_obj)
        else:
            return HttpResponse('内容不能为空')
    return render(request,"add_article.html")

#上传文件
from bbs import settings
import os
def upload(request):
    print(request.FILES)
    article_obj = request.FILES.get("upload_img")

    path = os.path.join(settings.MEDIA_ROOT,"article_obj_img",article_obj.name)
    with open(path,"wb") as f:
        for line in article_obj:
            f.write(line)
    res={
        "error":0,
        "url":"/media/article_obj_img/"+article_obj.name
    }

    return HttpResponse(json.dumps(res))