from django.shortcuts import render,HttpResponse,redirect
import json
from blog import models
from datetime import datetime
from blog.forms.modelforform import *
from collections import defaultdict
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from utils.comment_tackle import *
from blog.artical_views_count import artical_vews
from django.contrib.auth.decorators import  login_required
import requests
# @cache_page(60*15)
# @login_required
def index(request):
    if request.method=="GET":
        print("来普通请求了！！！！！！！！！！")
        #access times
        accesstimes=models.count.objects.all().count()
        print(accesstimes)
        artical_list=models.Artical.objects.all().order_by("-time")
        if  not cache.get('artical_list'):
            cache.set('artical_list',artical_list)
        paginator=Paginator(artical_list,4)
        page=request.GET.get('page')
        articals=paginator.get_page(page)

    return render(request, "blog/index.html",{'articals':articals,'count':accesstimes})

# @cache_page(60*15)
def miniartical(request):
    if request.is_ajax():
        print('来请求了！！！！！！！！')
        ret=defaultdict()
        mini_list=models.Artical.objects.all().order_by('-views').values('id','time','articalimg__imgfile','author','title')


        ret['mini']=list(mini_list)

        return HttpResponse(json.dumps(ret['mini'],cls=JsonCu))


class JsonCu(json.JSONEncoder):
    """JSON serializer for objects not serializable by default json code"""
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%b %d, %Y')
        elif isinstance(field, datetime.date):
            return field.strftime('%b %d, %Y')
        else:
            return json.JSONEncoder.default(self, field)

#文章详情
def artical_detail(request,aid):
    artical_obj=models.Artical.objects.get(id=aid)
    artical_vews.send(sender=artical_obj,**{'aid':aid})

    myform = commnetform()

    return render(request,"blog/artical_detail.html",{"artical_obj":artical_obj,'myform':myform,})

def comment_tackle(request,aid):
    comment_list = models.comment.objects.filter(artical_id=aid).values()
    result_commnet = gender_comment(list(comment_list))
    return render(request,'blog/comment_tem.html',{'comment':result_commnet,"comment_long":len(list(comment_list))})


def usercomment(request):
    user=request.POST.get('user')
    artical_id=request.POST.get('artical')
    content=request.POST.get('content')
    print(user,artical_id,content)
    models.comment.objects.create(user=request.user,
                                  artical=models.Artical.objects.get(id=int(artical_id)),
                                  content=content,
                                  )
    return redirect("/artical/artical_id={}".format(artical_id))


#userlogin



def all_artical(request):
    # print(cache.get('artical_list'))
    return HttpResponse('ok')

def technology(request):
    return HttpResponse('technology')

def essay(request):
    return HttpResponse('essay')