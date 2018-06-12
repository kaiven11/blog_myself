from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from utils.user_img import *
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import options
# Create your models here.
class Artical(models.Model):

    title=models.CharField(max_length=600,unique=True)
    content=RichTextUploadingField(null=True,blank=True)
    time=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField('Tags',)
    author=models.ForeignKey('UserProfile',on_delete=models.CASCADE,null=True)
    views=models.PositiveIntegerField(null=True)
    describe=models.CharField(max_length=128,null=True)
    category=models.ForeignKey('category',null=True,blank=True,on_delete=models.DO_NOTHING)
    def __str__(self):
        return  self.title


    class Meta:
        verbose_name="文章表"
        verbose_name_plural="文章表"


#图片预览
class Review(models.Model):
    picture = models.ForeignKey("articalimg", verbose_name=("Picture"), on_delete=models.CASCADE)
    reviewer = models.CharField(("Reviewer name"), max_length=255)
    comment = models.TextField(("Comment"))
    category=models.ForeignKey('category',on_delete=models.DO_NOTHING,null=True)
    class Meta:
        verbose_name = ("Review")
        verbose_name_plural = ("Reviews")

    def __str__(self):
        return self.reviewer


#分类
class category(models.Model):
    title=models.TextField(max_length=64)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name="分类"
        verbose_name_plural="分类"

#评论表
class comment(models.Model):
    artical=models.ForeignKey('Artical',on_delete=models.DO_NOTHING)
    parent=models.ForeignKey('self',to_field='id',related_name='parent_comment',null=True,blank=True,on_delete=models.DO_NOTHING)
    content=RichTextUploadingField(help_text="<a>请登陆后在进行评论<a>")
    user=models.ForeignKey('UserProfile',on_delete=models.DO_NOTHING)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.content)
    class Meta:
        verbose_name = "评论表"
        verbose_name_plural = "评论表"
        get_latest_by='time'
        ordering=['time']

#图片
class articalimg(models.Model):
    artical=models.ForeignKey("Artical",on_delete=models.CASCADE)
    imgfile=models.ImageField(upload_to=User_directory_path,null=True)
    title=models.CharField(max_length=64)
    def get_edit_link(self,obj=None):
        print(type(obj), "get_edit_link")
        if self.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.pk])
            return mark_safe("""<a href="{url}">{text}</a>""".format(
                url=url,
                text=("Edit this %s separately") % self._meta.verbose_name,
            ))
        return mark_safe("(save and continue editing to create a link)")

    get_edit_link.short_description = ("Edit link")
    get_edit_link.allow_tags = True
    class Meta:
        verbose_name="文章图片"
        verbose_name_plural="文章图片"
    def __str__(self):
        return self.title

class Tags(models.Model):
    title=models.CharField(max_length=64)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="标签分类"
        verbose_name="标签分类"


#user for git
# class GitHub(models.Model):
#     user=models.OneToOneField("UserProfile",on_delete=models.CASCADE)
#     avatar=models.URLField()
#     github_id=models.PositiveIntegerField()



class MyUserManager(BaseUserManager):
    def create_user(self, github_id, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not github_id:
            raise ValueError('Users must have an github_id')

        user = self.model(
            github_id=github_id,
            name=name,
        )

        user.set_password(password)
        self.is_active = True

        user.save(using=self._db)
        return user

    def create_superuser(self, github_id, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            github_id=github_id,
            password=password,
            name=name,
        )
        user.is_admin = True
        self.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''博客系统用户'''
    password = models.CharField(('password'), max_length=128,help_text=mark_safe('''<a href="password/">重置密码</a>'''))# 重写继承类的pasword
    name = models.CharField(max_length=32)
    avatar = models.URLField(null=True,blank=True)
    github_id = models.PositiveIntegerField(null=True,unique=True)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    img_for_user=models.ImageField(upload_to=artical_img_path,null=True,default="/aa.jpg")
    USERNAME_FIELD = 'github_id'
    REQUIRED_FIELDS = ['name'] #just effect when create the super user
    #--------when you custom a user model,if you want the django admin access the model
            #you should define the follow fileds
    # --------------------------------------
    def get_full_name(self):
        # The user is identified by their email address
        return self.github_id

    def get_short_name(self):
        # The user is identified by their email address
        return self.github_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    #-------------------------------------
    def __str__(self):
         return self.name
    class Meta:
        verbose_name="用户表"
        verbose_name_plural="用户表"

    def save(self, *args, **kwargs):
        # super().save()
        if self.img_for_user.url:
            self.avatar=self.img_for_user.url
        super().save(*args, **kwargs)
