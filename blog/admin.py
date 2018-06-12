from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from blog.models import *
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('github_id','avatar','name', "is_active","is_staff",'is_admin','img_for_user')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('Personal info', {'fields': ('name','img_for_user','avatar')}),
        ('Permissions', {'fields': ('is_admin',"is_active",'is_superuser',"user_permissions","groups",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('avatar', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ("user_permissions","groups",)


def get_picture_preview(obj):
    print(type(obj),"get_pictrue,review")
    if obj.pk:  # if object has already been saved and has a primary key, show picture preview
        print(obj.imgfile.url,'----------->')
        return mark_safe(
            """<a href="{src}" target="_blank"><img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" /></a>""".format(
                src=obj.imgfile.url,

                title=obj.title,
            ))
    return mark_safe("(choose a picture and save and continue editing to see the preview)")
get_picture_preview.allow_tags = True
get_picture_preview.short_description = ("Picture Preview")







def get_test_aa(obj):
    if obj.pk:
        print(type(obj))

    return "(asdfsd)"
get_test_aa.allow_tags = True
get_test_aa.short_description = ("test")

class ImageInline(admin.StackedInline):
    model = articalimg
    extra = 0
    fields = ['get_edit_link', "title",'imgfile',get_picture_preview ,get_test_aa]
    readonly_fields = ['get_edit_link',get_picture_preview,get_test_aa,]

class reviewInline(admin.StackedInline):
    model = Review
    extra = 0#For users with JavaScript-enabled browsers,
             #  an “Add another” link is provided to enable any number of additional inlines to be added in addition to those provided as a result of the extra argument.
    fields = ['comment','reviewer']

class articalimgAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ["title",'imgfile','artical', get_picture_preview]
    readonly_fields = [get_picture_preview]
    inlines = [reviewInline]
@admin.register(Artical)
class ArticalAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title','time','views','category',)
    inlines = [ImageInline]

    # class Media:
    #     # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
    #     js = (
    #         '/static/js/kindeditor/kindeditor-all-min.js',
    #         # '/static/js/kindeditor/zh_CN.js',
    #         '/static/js/kindeditor/config.js',
    #     )

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content','parent','time',]




# admin.site.register(Artical,ArticalAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(articalimg,articalimgAdmin)
admin.site.register(Tags)
# admin.site.register(comment)
admin.site.register(Review)
