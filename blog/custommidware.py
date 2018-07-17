#coding=utf-8
import time
from blog import models

class MyMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class count_midware(MyMiddleware):


    def process_request(self, request):
        print(request.META)
        date=time.strftime("%Y-%m-%d",time.localtime())
        access_ip=request.META['REMOTE_ADDR']
        models.count.objects.get_or_create(date=date,IP=access_ip)#更新数据表











    # def process_response(self, request, response):
    #     pass




