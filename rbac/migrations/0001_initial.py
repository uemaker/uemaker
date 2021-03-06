# Generated by Django 2.1 on 2018-09-18 09:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='用户组标识')),
                ('title', models.CharField(max_length=20, verbose_name='用户组名称')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组列表',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='权限名称')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='权限编码')),
            ],
            options={
                'verbose_name': '权限资源',
                'verbose_name_plural': '权限资源列表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='用户ID')),
                ('username', models.CharField(error_messages={'unique': '该用户名已存在'}, help_text='用户名最长为20个字符', max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='邮箱')),
                ('real_name', models.CharField(blank=True, max_length=20, verbose_name='真实姓名')),
                ('is_active', models.BooleanField(default=True, help_text='未启用的用户将无法登录系统. ', verbose_name='是否启用')),
                ('is_super', models.BooleanField(default=False, help_text='超级管理员拥有最高权限，请谨慎授权 ', verbose_name='超级管理员')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='最后登录')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='用户将拥有所有组的权限 ', related_name='user_set', related_query_name='user', to='rbac.Group', verbose_name='用户所属组')),
                ('permissions', models.ManyToManyField(blank=True, help_text='用户拥有的所有权限', related_name='user_set', related_query_name='user', to='rbac.Permission', verbose_name='用户权限')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户列表',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='权限列表'),
        ),
    ]
