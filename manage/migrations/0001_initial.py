# Generated by Django 2.1 on 2018-09-17 06:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cat_id', models.IntegerField(verbose_name='分类ID')),
                ('title', models.CharField(error_messages={'max_length': '标题最长为100个字符', 'required': '请输入标题'}, max_length=100, verbose_name='标题')),
                ('desc', models.CharField(error_messages={'max_length': '简介最长为200个字符', 'required': '请输入简介'}, max_length=255, verbose_name='简介')),
                ('user_id', models.BigIntegerField(default=0, verbose_name='用户ID')),
                ('author', models.CharField(blank=True, max_length=20, verbose_name='作者')),
                ('source', models.CharField(blank=True, max_length=200, verbose_name='来源')),
                ('status', models.SmallIntegerField(default=0, verbose_name='状态')),
                ('cover', models.FileField(blank=True, upload_to='', verbose_name='封面图')),
                ('pub_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发表时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章列表',
                'db_table': 'article',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleContent',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='内容')),
            ],
            options={
                'verbose_name': '内容',
                'verbose_name_plural': '内容列表',
                'db_table': 'article_content',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(error_messages={'max_length': '英文名称最长为20个字符', 'required': '请输入英文名称', 'unique': '英文名称已存在'}, max_length=20, unique=True, verbose_name='英文名称')),
                ('title', models.CharField(error_messages={'max_length': '中文名称最长为20个字符', 'required': '请输入中文名称'}, max_length=20, verbose_name='中文名称')),
                ('pid', models.IntegerField(default=0, verbose_name='上级分类')),
                ('path', models.CharField(blank=True, default='', max_length=255, verbose_name='路径')),
                ('module_id', models.IntegerField(default=0, verbose_name='模块ID')),
                ('config', models.CharField(blank=True, default='', max_length=255, verbose_name='配置信息')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类列表',
                'db_table': 'category',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldItem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('module_id', models.IntegerField(verbose_name='模块ID')),
                ('field_id', models.IntegerField(verbose_name='字段ID')),
                ('object_id', models.BigIntegerField(verbose_name='模型对象ID')),
                ('content', models.CharField(max_length=255, verbose_name='字段内容')),
            ],
            options={
                'verbose_name': '字段内容',
                'verbose_name_plural': '字段内容列表',
                'db_table': 'field_item',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(error_messages={'max_length': '标识最长为20个字符', 'required': '请填写标识', 'unique': '标识名已存在'}, max_length=20, unique=True, verbose_name='模块标识')),
                ('title', models.CharField(max_length=20, verbose_name='模块名称')),
                ('matrix', models.CharField(blank=True, max_length=20, verbose_name='模型')),
                ('is_system', models.BooleanField(default=False, verbose_name='系统模块')),
                ('desc', models.CharField(blank=True, max_length=200, verbose_name='模块介绍')),
                ('config', models.CharField(blank=True, max_length=255, verbose_name='配置')),
            ],
            options={
                'verbose_name': '模块',
                'verbose_name_plural': '模块列表',
                'db_table': 'module',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModuleField',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('module_id', models.IntegerField(verbose_name='模块ID')),
                ('type', models.CharField(max_length=20, verbose_name='字段类型')),
                ('name', models.CharField(error_messages={'max_length': '标识最长为20个字符', 'required': '请输入标识'}, max_length=20, verbose_name='字段名称')),
                ('title', models.CharField(error_messages={'max_length': '名称最长为20个字符', 'required': '请输入名称'}, max_length=20, verbose_name='字段说明')),
                ('length', models.SmallIntegerField(verbose_name='字段长度')),
                ('blank', models.BooleanField(blank=True, default=True, verbose_name='是否必填')),
                ('default', models.CharField(blank=True, max_length=100, verbose_name='默认值')),
                ('help_text', models.CharField(blank=True, max_length=100, verbose_name='帮助提示')),
                ('value', models.CharField(blank=True, max_length=200, verbose_name='选项')),
                ('sort', models.IntegerField(blank=True, default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '模块字段',
                'verbose_name_plural': '模块字段列表',
                'db_table': 'module_field',
                'abstract': False,
            },
        ),
    ]
