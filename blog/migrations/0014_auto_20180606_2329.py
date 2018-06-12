# Generated by Django 2.0.5 on 2018-06-06 15:29

import ckeditor_uploader.fields
from django.db import migrations, models
import utils.user_img


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20180601_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(max_length=64)),
                ('avatar', models.URLField()),
                ('github_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': 'time', 'ordering': ['time'], 'verbose_name': '评论表', 'verbose_name_plural': '评论表'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='<a>请登陆后在进行评论<a>'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='img_for_user',
            field=models.ImageField(default='/aa.jpg', null=True, upload_to=utils.user_img.artical_img_path),
        ),
    ]
