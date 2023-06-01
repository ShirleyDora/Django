Shirley-2023/05/02开始

#一、使用说明：
1.运行方式: python3 manage.py runserver
2.前端网址: http://127.0.0.1:8000/index/
3.后端网址: http://127.0.0.1:8000/admin/
4.后台:账号:admin,密码:admin123456;
5.前台:账号:Shirley,密码:Shirley123456
6.数据库：需要本地安装mysql
7.单元测试：python3 manage.py test
8.接口测试: pybot test.robot

#二、功能:
发布会管理系统，前端Django-bootstrap3,后端Django,数据库SQLite3/PyMySQL,测试框架：unittest，postman,JMeter,Robot Framework,Requests,HTMLTestRunner,soapUI,Locust,部署uWSGI,Nginx。
共4个功能包含1.发布会管理：发布会列表，搜索功能；2.嘉宾管理：嘉宾列表，分页器；3.签到功能：添加签到链接，签到页面，签到动作；4.退出系统。

#三、理解：
##1.
UI-UI界面层-UI自动化测试+JS自动化测试+手工测试
Service-业务逻辑层-集成接口测试+web接口测试
Unit-数据处理层-模块/单元测试+Code Review
##2.HTTP
GET/POST/HEAD（类似GET请求，获取报文头）/PUT/DELETE/TRACE(用于测试或诊断，分析性能）/CONNECT/OPTIONS（查服务器性能或资源）
1**：信息，2**：成功，3**：重定向，4**：客户端前端错误，5**:服务端后端错误
200 OK:请求成功；302 Fund:临时移动；400 Bad Request:客户端前端语法错误；401 Unauthorized:用户身份认证缺失；403 Forbidden:服务器理解但拒绝执行；404 Not Found:服务器无法找到资源；500 Internal Server Error:服务器内部错误；503 Server Unavailable:超载或系统维护，服务器无法处理请求

#四、更新历史:
2023/05/02 数据库采用Django默认使用Python自带的SQLite3,不适用大型项目
2023/05/03 迁移数据库到MySQL,使用PyMySQL,添加1.发布会管理 
2023/05/04 添加2.嘉宾管理：嘉宾列表，分页器；3.签到功能：添加签到链接，签到页面，签到动作；4.退出系统。
2023/05/05 优化代码,css,js,添加单元测试unittest框架见tests.py
2023/05.06 添加接口测试

#五、接口文档
举例部分：
1.添加发布会接口
名称：添加发布会
URL:http://127.0.0.1:8000/api/add_event/
调用方法：POST
传入参数:eid #发布会id
        name #发布会标题
        limit #限制人数
        status #状态（非必填）
        address #地址
        start_time #发布会时间（格式:2023-05-06 12:00:00)
返回值:{
        'status':200,
        'message':'add event success'
        }
状态码:10021:parameter error
       10022:event id already exists
       10023:event name already exists
       10024:start_time format error.It must be in YYYY-MM-DD HH:MM:SS formate.
       200:add event success
说明：无
2.查询发布会接口
名称：查询发布会接口
URL:http://127.0.0.1:8000/api/get_event_list/
调用方法：GET
传入参数:eid #发布会id
        name #发布会名称
返回值:{
        "data":{
            "start_time":"2023-05-06T14:00:00',
            "name":"小米手机6发布会",
            "limit":2000,
            "address":"北京水立方",
            "status":true
        },
        "message":"success",
        "status":200
        }
状态码:10021:parameter error
       10022:query result is empty
       200:success
说明:eid或name两个参数二选一
3.添加嘉宾接口
名称：添加嘉宾接口
URL:http://127.0.0.1:8000/api/add_guest/
调用方法：POST
传入参数:eid #发布会id
        realname #姓名
        limit #限制人数
        phone #手机号
        email #邮箱
返回值:{
        'status':200,
        'message':'add guest success'
        }
状态码:10021:parameter error
       10022:event id null
       10023:event status is not available
       10024:event number is full
       10025:event has started
       10026:the event guest phone number repeat
       200:add guest success
说明：无
4.查询嘉宾接口
名称：查询嘉宾接口
URL:http://127.0.0.1:8000/api/get_guest_list/
调用方法：GET
传入参数:eid #发布会id
        phone #嘉宾手机号
返回值:{
        "data":[
            {
                "email":"david@mail.com",
                "phone":"13800110005",
                "realname":"david",
                "sign":false
            },
            {
                "email":"david@mail.com",
                "phone":"13800110005",
                "realname":"david",
                "sign":false
            },
            {
                "email":"david@mail.com",
                "phone":"13800110005",
                "realname":"david",
                "sign":false
            },
        ]
        "message":"success",
        "status":200
        }
状态码:10021:eid cannot be empty
       10022:query result is empty
       200:success
说明:无
5.发布会签到接口
名称：发布会签到接口
URL:http://127.0.0.1:8000/api/user_sign/
调用方法：GET
传入参数:eid #发布会id
        phone #手机号
返回值:{
        'status':200,
        'message':'sign success'
        }
状态码:10021:parameter error
       10022:event id null
       10023:event status is not available
       10024:event has started
       10025:user phone null
       10026:user did not participate in the conference
       10027:user has sign in
       200:sign success
说明：无