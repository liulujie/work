from django.shortcuts import render

# Create your views here.
from django.views import View

# 定义视图函数IndexView,继承View并调用里面的get方法
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        return render(request, 'index.html')
