from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User
# Create your tests here.
# class ModelTest(TestCase):
#     def setUp(self):
#         Event.objects.create(id=1,name="oneplus 3 event",status=True,limit=2000,address="shenzhen",start_time='2023-05-05 22:10:00')
#         Guest.objects.create(id=1,event_id=1,realname='alen',phone='13711001101',email='alen@mail.com',sign=False)
#     def test_event_models(self):
#         result = Event.objects.get(name="oneplus 3 event")
#         self.assertEqual(result.address,"shenzhen")
#         self.assertTrue(result.status)
#     def test_guest_models(self):
#         result = Guest.objects.get(phone='13711001101')
#         self.assertEqual(result.realname,"alen")
#         self.assertFalse(result.sign)
# 测试首页
class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')
#测试登录动作
class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
    # 测试添加用户
    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,'admin@mail.com')
    # 用户名密码为空
    def test_login_action_username_password_null(self):
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/',data = test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error!",response.content)
    # 用户名密码错误
    def test_login_action_username_password_error(self):
        test_data = {'username':'abc','password':'123'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error!",response.content)
    # 登录成功
    def test_login_action_success(self):
        test_data = {'username':'admin','password':'admin123456'}
        response = self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)
# 测试发布会管理
class EventMangeTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(name="xiaomi5",limit=2000,address="beijing",status=1,start_time="2023-05-05 12:30:00")
        self.login_user={'username':'admin','password':'admin123456'}
    # 测试发布会小米5
    def test_event_manage_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"beijing",response.content)
    # 测试发布会搜索
    def test_event_manage_search_success(self):
        response = self.client.post('/login_action',data=self.login_user)
        response = self.client.post('/search_name',{"name":"xiaomi5"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"beijing",response.content)
# 测试嘉宾管理
class GuestManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(name="xiaomi5",limit=2000,address="beijing",status=1,start_time="2023-05-05 12:30:00")
        Guest.objects.create(realname="alen",phone=18611001100,email="alen@mail.com",sign=0,event_id=1)
        self.login_user={'username':'admin','password':'admin123456'}
    # 测试嘉宾信息:alen
    def test_event_manage_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"alen",response.content)
        self.assertIn(b"18611001100",response.content)
    # 测试嘉宾搜索(需要先完成被测功能)
    def test_guest_manage_search_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/search_phone/',{"phone":"18611001100"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"alen",response.content)
        self.assertIn(b"18611001100",response.content)
# 测试用户签到
class SignIndexActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address="beijing",status=1,start_time="2023-05-05 12:30:00")
        Event.objects.create(id=2,name="oneplus4",limit=2000,address="shenzhen",status=1,start_time="2023-05-05 22:30:00")
        Guest.objects.create(realname="alen",phone=18611001100,email="alen@mail.com",sign=0,event_id=1)
        Guest.objects.create(realname="una",phone=18611001101,email="una@mail.com",sign=1,event_id=2)
        self.login_user={'username':'admin','password':'admin123456'}
    # 手机号为空
    def test_sign_index_action_phone_null(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{"phone":""})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"phone error.",response.content)
    # 手机号或发布会id错误
    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{"phone":"18611001100"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"event id or phone error.",response.content)
    # 用户已签到
    def test_sign_index_action_user_sign_has(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/2/',{"phone":"18611001101"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"user has sign in.",response.content)
    # 签到成功
    def test_sign_index_action_sign_success(self):
        response = self.client.post('/login_action/',data=self.login_user)
        response = self.client.post('/sign_index_action/1/',{"phone":"18611001100"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"sign in success!",response.content)