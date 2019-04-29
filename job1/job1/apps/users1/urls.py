from django.conf.urls import url

# from . import views
from . import views

urlpatterns = [
# as_view?
    #as_view 将类视图转换为实例对象
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

# 判断用户名是否重复
url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
]
