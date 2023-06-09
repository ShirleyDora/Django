# from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
# 首页(登录)
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request,"index.html")
# 登录动作
def login_action(request):
    if request.method == 'POST':
         # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username == '' or password == '':
            return render(request,"index.html",{"error":"username or password null!"})
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
            request.session['username']=username
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
#  发布会管理（登录后的第一个页面）
# bug:直接浏览器访问:http://127.0.0.1:8000/event_manage/也可以登录，已修复，bugfixed添加装饰器
@login_required
def event_manage(request):
    #发布会列表
    event_list = Event.objects.all()
    #读取浏览器cookie
    # username = request.COOKIES.get('user','')
    # 读取浏览器sesstion
    username = request.session.get('username','')
    # return render(request,'event_manage.html')     
    # return render(request,"event_manage.html",{"user":username})  
    return render(request,"event_manage.html",{"user":username,"events":event_list})  
# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('username','')
    search_name = request.GET.get("name","")
    search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage.html", {"user": username, "events": event_list})
# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('username','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果page不是整数，取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        #如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})
# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username,"guests": contacts,"phone":search_phone})
# 签到页面
# @login_required
# def sign_index(request,eid):
#     event = get_object_or_404(Event,id=eid)
#     return render(request,'sign_index.html',{'event':event})
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)           # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=eid)   # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,'guest':guest_data,'sign':sign_data})
# 前端签到页面2
def sign_index2(request,eid):
    event_name = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index2.html',{'eventId': eid,
                                               'eventName': event_name})

# 签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    guest_data = str(len(guest_list))
    sign_data = 0   #计算发布会“已签到”的数量
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1
    phone =  request.POST.get('phone','')
    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})
    result = Guest.objects.filter(phone = phone,event_id = eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})
    result = Guest.objects.get(event_id = eid,phone = phone)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = eid,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'user': result,
            'guest':guest_data,
            'sign':str(int(sign_data)+1)
            })
    
'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''
# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response