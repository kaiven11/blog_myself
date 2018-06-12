from django.shortcuts import render,redirect,HttpResponse
from auth.settings import *
import requests
from blog.models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Q

#用户点击登陆后跳转
def userlogin(request):
    if request.method=="GET":
        request.session['next']=request.GET.get('next','/index')

        return render(request,"blog/acount/login.html",)

def userlogout(request):
    logout(request)
    return redirect('/index')


def gihublogin(request):
    if request.method=="GET":
        code=request.GET.get('code')
        data={'code':code,
              'client_id':CLIENT_ID,
              "client_secret":ClIENT_SECRET,
              }
        r=requests.post(ACCESS_TOKEN_URL,json=data,)
        param=str(r.content,encoding="utf-8")
        if r.status_code==200:

            ret=requests.get(USER_API,params=param)
            id=ret.json()['id']
            username=ret.json()['login']
            avatar_url=ret.json()['avatar_url']
            password=ret.json()['id']
            user,created = UserProfile.objects.get_or_create(github_id=id,name=username,defaults={"password":"tttt"})
            if created:
                user.set_password('aaaaaaa')
                print("执行了")
            print(user, dir(user), type(user),created)
            if user:

                request.user=user
                login(request,request.user)
                return redirect(request.session['next'])
    return HttpResponse(r.content)
