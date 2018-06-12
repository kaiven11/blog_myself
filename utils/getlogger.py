#coding=utf-8

import logging
def checkargs(cls):
    '''
    :param cls: the class which need to check args
    :return: cls(*args,**kwargs)
    '''
    def wrapper(*args,**kwargs):

        if not "stream" in kwargs and not "File" in kwargs:
            kwargs["stream"]=True
        if "stream" in kwargs and kwargs['stream']:
            if "File" in kwargs:
                kwargs.pop('File')
            if 'path' in kwargs:
                kwargs.pop('path')
        else:
            if not "File" in kwargs or not "path" in kwargs:
                raise ValueError("Lack Arguments of  %s or %s "%("path",'File'))
        return  cls(*args,**kwargs)
    return  wrapper

@checkargs
class get_logger:
    """
    This class use to get logging object depend on what input
    if the arg of File set,the path need, if the arg of stream and File set at the same time,
    will use the arg of stream as the default.

    :param loggername  the logger name
    :param level the logger level
    :param stream or File streamhandler or Filehandler
    """
    def __init__(self,loggername,level,stream=False,File=False,path=None):
        self.stream=stream
        self.File=File
        self.level=level
        self.path=path
        self.loggername=loggername
        self.logger = logging.getLogger(self.loggername)
        self.handler=None
        self.fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.parse_args()
    def parse_args(self):
        if self.stream:
            self.handler=logging.StreamHandler()
        else:
            self.handler=logging.FileHandler(self.path)
        self.get_instance()

    def get_instance(self):
        self.logger.setLevel(self.level)
        self.handler.setLevel(self.level)

        self.handler.setFormatter(self.fmt)
        self.logger.addHandler(self.handler)

    def info(self,msg,*args,**kwargs):
        self.logger.info(msg,*args,**kwargs)

    def debug(self,msg,*args,**kwargs):
        self.logger.debug(msg,*args,**kwargs)

    def warning(self,msg,*args,**kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def exception(self,msg,*args,**kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def critical(self,msg,*args,**kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def error(self,msg,*args,**kwargs):
        self.logger.error(msg, *args, **kwargs)



if __name__=="__main__":
    logger=get_logger("mylog",level=logging.WARNING,File=True,stream=True)
    logger.error('test')






