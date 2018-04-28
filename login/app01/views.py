# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect
from app01.models import User
from app01.forms import Zhuce

# Create your views here.
def index(request):
    if request.method == "GET":
        fm = Zhuce()
    elif request.method == "POST":
        fm = Zhuce(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/index")
        else:
            if user.password == password:
                return HttpResponseRedirect("/login")
            else:
                return HttpResponseRedirect("/index")

    return render(request, "index.html",locals())

def zhuce(request):
    if request.method == "GET":
        fm = Zhuce()

    elif request.method == "POST":
        fm = Zhuce()
        # 获取值
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        #实例化数据库
        user = User()
        user.username = username
        user.password = password
        user.save()

        return render(request, "index.html", locals())
    return render(request, "zhuce.html" ,locals())



def login(request):
    return render(request, "login.html")