Shirley-2023/05/02开始

#一、使用说明：
1.运行方式: python3 manage.py runserver
2.前端网址: http://127.0.0.1:8000/index/
3.后端网址: http://127.0.0.1:8000/admin/
4.后台:账号:admin,密码:admin123456;
5.前台:账号:Shirley,密码:Shirley123456
6.数据库：需要本地安装mysql

#二、功能:
发布会管理系统，前端Django-bootstrap3,后端Django,数据库SQLite3/PyMySQL,测试框架：unittest，postman,JMeter,Robot Framework,Requests,HTMLTestRunner,soapUI,Locust,部署uWSGI,Nginx。
共4个功能包含1.发布会管理：发布会列表，搜索功能；2.嘉宾管理：嘉宾列表，分页器；3.签到功能：添加签到链接，签到页面，签到动作；4.退出系统。

#三、更新历史:
2023/05/02 数据库采用Django默认使用Python自带的SQLite3,不适用大型项目
2023/05/03 迁移数据库到MySQL,使用PyMySQL,添加1.发布会管理 
2023/05/04 添加2.嘉宾管理：嘉宾列表，分页器；3.签到功能：添加签到链接，签到页面，签到动作；4.退出系统。
2023/05/05 优化代码,css,js