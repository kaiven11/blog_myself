# #coding=utf-8
from django.forms import ModelForm
from blog.models import comment
from django.forms import widgets as MFwidgets

class commnetform(ModelForm):
    class Meta:
        model=comment
        fields=['content']
        labels={'content':''}

