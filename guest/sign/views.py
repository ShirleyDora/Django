# from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event

# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request,"index.html")
# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        # if username == 'admin' and password == 'admin123':
        if user is not None:
            # 配置了数据库后的登录
            auth.login(request,user)
            # return HttpResponse('login success!')
            # 重定向
            # return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')
            #添加浏览器cookie不安全
            # response.set_cookie('user',username,3600) 
            #将session信息记录到浏览器
            request.session['user']=username
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
#  发布会管理
# bug:直接浏览器访问:http://127.0.0.1:8000/event_manage/也可以登录，已修复，bugfixed添加装饰器
@login_required
def event_manage(request):
    #发布会列表
    event_list = Event.objects.all()
    #读取浏览器cookie
    # username = request.COOKIES.get('user','')
    # 读取浏览器sesstion
    username = request.session.get('user','')
    # return render(request,'event_manage.html')     
    # return render(request,"event_manage.html",{"user":username})  
    return render(request,"event_manage.html",{"user":username,"events":event_list})  
# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})