"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from blog import views


from django.views import static
from django.conf import settings
# from django.views import
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index,name="index_view"),
    path('',views.index,name="index_view"),
    path('miniartical/',views.miniartical,name="miniartical"),
    path(r'artical/artical_id=<int:aid>',views.artical_detail,name="detail_artical"),
    re_path(r'ckeditor/',include('ckeditor_uploader.urls')),
    path(r'all_artical/',views.all_artical,name='all_artical'),
    path(r'technology/',views.technology,name='technology'),
    path(r'essay/',views.essay,name='essay'),
    path(r'oauth/',include("auth.urls")),
    path(r'account/',include("auth.urls")),
    path(r'comment/<int:aid>',views.comment_tackle,name='comment_tackle'),
    path(r'/post/comment',views.usercomment,name='usercomment'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

