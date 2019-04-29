# from audioop import reverse
import re

from django import http
from django.contrib.auth import login
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from job1.utils.response_code import RETCODE
from . models import User



class UsernameCountView(View):
    """判断用户名是否重复注册"""

# 调用view里的get函数,并获取路径里username传入的参数信息
    def get(self, request, username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: JSON
        """
        # 创建count对象,通过filter条件过滤的方式,调用count函数,判断用户是否重复,0,继续注册,1提示用户已存在
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})







# 创建一个类视图,继承View
class RegisterView(View):
    """用户注册"""

    # 接受客户端注册的请求并返回对应的注册界面
    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self, request):
        # 实现用户注册
        #接受表单传过来的参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

    # 效验参数,判断参数是否规范齐全
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')

        # 保存注册数据
        try:
            # 调用create-user对信息加密
            user =User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            # 若信息有误,则返回到register页面,并以字典的方式返回错误提示信息
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 调用封装有session的login函数将用户登录状态保存
        login(request, user)


        # 响应注册结果
        #解析别名并重定向
        return redirect(reverse('contents:index'))











