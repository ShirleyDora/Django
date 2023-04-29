"""guest URL Configuration
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
from django.contrib import admin
from sign import views #导入sign应用views文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',views.index), #添加index/路径配置
    url(r'^login_action/$',views.login_action),
]