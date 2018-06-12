#coding=utf-8
import os

BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_PATH)
#自动将图片保存在相应文章的目录下
def User_directory_path(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    basepath= "articals/{artical}/".format(
        artical=(instance.artical.title),
    )
    path= "articals/{artical}/{filename}{extension}".format(
        artical=(instance.artical.title),
        filename=(filename_base),
        extension=filename_ext.lower(),
    )
    img_relpath=os.path.join(BASE_PATH,'media',basepath)
    if not os.path.exists(img_relpath):
        return path
    if os.listdir(img_relpath):
        for i in os.listdir(img_relpath):
            try:
                os.remove(os.path.join(img_relpath,i))
            except:
                continue



    return path

def artical_img_path(instance,filename):
    filename_base, filename_ext = os.path.splitext(filename)
    print(instance,filename)
    return "user/{username}/{filename}{extension}".format(
        username=(instance.email),
        filename=(filename_base),
        extension=filename_ext.lower(),
    )