#coding=utf-8
import django.dispatch
artical_vews=django.dispatch.Signal(providing_args=['aid'])

def my_callback(**kwargs):
    obj=kwargs['sender']
    obj.views+=1
    obj.save()
artical_vews.connect(my_callback)