#coding=utf-8
import logging
from django import template
from django.utils.safestring import mark_safe
from django.core.cache import cache
from utils.getlogger import get_logger
from w3lib.html import remove_tags
from blog.models import *
import time
import re

from collections import deque
from django.template.loader import get_template
logger=get_logger("mylog",level=logging.DEBUG,stream=True)
register=template.Library()



@register.simple_tag
def cache_content(arg):
    '''cache the content one part '''
    short_discription,last_content=arg.content[:200],arg.content[200:]
    # cache.set(arg.id,re.sub('<p>|</p>',"",last_content))
    return mark_safe(remove_tags(short_discription)+"{}".format('.'*10))

@register.filter
def tackleimg(item):
    '''if the artical has no imgage ,skip the tag "<a href=..." '''
    logger.info(item.articalimg_set.all())
    if len(item.articalimg_set.all())>0 :
       logger.info("yes")
       return  True
    else:
        return False


result=''

tem_html="""<li class="comment-item">
        <a class="avatar">
             
            <img src="https://avatars1.githubusercontent.com/u/37147531?v=4 " atl="avator">  
        </a>
        <a class="username">{username}</a>
        <span style="float: right;">#3</span>
        <div class="content">{content}</div>
        <span>{datetime}&emsp;</span>
        <span class="reply-this" data-comment-id={contentid} data-user-id="12">
            <i class="fa fa-reply"></i> 回复</span>
        <ul class="reply-list">
            
        </ul>
    </li>"""



@register.simple_tag

def gencomment(comment_list,comment_long):

        html = '<div class="comment_list" value={}>'.format(comment_long)
        for k,v in enumerate(comment_list):
            print(v,'vvvvvvvvvvvvv')
            a = '<div class="comment_item"><span>'
            a+='<span><img src={imgurl} height=18px width=18px/></span><span>{username}:</span>'.format(imgurl=UserProfile.objects.get(id=v['user_id']).avatar,username=UserProfile.objects.get(id=v['user_id']).name)
            a+="<span class=lou>#{}</span>".format(k)
            a += v['content'] + '</span>'
            print(type(comment.objects.get(id=v['id']).time),dir(comment.objects.get(id=v['id']).time))

            a+='<span style="color:gray">{datetime}&emsp;</span>'.format(datetime=(comment.objects.get(id=v['id']).time.strftime("%Y-%m-%d %H:%M:%S")))
            a+='<a class="reply" id="reply_conmment" href=javascript:void(0)>回复</a>'
            a += DiGui(v['include'])
            a += ''
            html += a
            html = html + '</div>'

        return mark_safe(html)



def DiGui(children_list):

        html = ''
        for cv in children_list:
            b = '<div class="replay_item"><span>'
            b+= '<span><img src={imgurl} height=18px width=18px/></span><span>{username}:</span>'.format(
                imgurl=UserProfile.objects.get(id=cv['user_id']).avatar,
                username=UserProfile.objects.get(id=cv['user_id']).name)
            b+='<span>{username}:'.format(username=UserProfile.objects.get(id=cv['user_id']).name)
            b += cv['content'] + '</span>'
            b+='<span style="color:gray">{datetime}&emsp;</span>'.format(datetime=(comment.objects.get(id=cv['id']).time.strftime("%Y-%m-%d %H:%M:%S")))
            b += '<a class="reply" id="reply_conmment" href=javascript:void(0)>回复</a>'
            b += DiGui(cv['include'])

            html = html + b + '</div>'
        return html
