import unicodedata
from django.db import models
from django.contrib.auth import hashers


# Create your models here.
from django.utils import timezone


class UserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

    def get_by_name(self, username):
        return self.get(username=username)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(u'用户名不能为空')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_super', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_super', True)
        if extra_fields.get('is_super') is not True:
            raise ValueError('超级管理员必须设置is_super=True.')
        return self._create_user(username, email, password, **extra_fields)

    def check_password(self, raw_password):

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return hashers.check_password(raw_password, self.password, setter)


class User(models.Model):
    id = models.BigAutoField(verbose_name=u'用户ID', primary_key=True)
    username = models.CharField(
        verbose_name=u'用户名',
        max_length=20,
        unique=True,
        help_text=u'用户名最长为20个字符',
        error_messages={
            'unique': '该用户名已存在',
        },
    )
    password = models.CharField(verbose_name=u'密码', max_length=128)
    email = models.EmailField(verbose_name=u'邮箱', blank=True)
    real_name = models.CharField(verbose_name=u'真实姓名', max_length=20, blank=True)
    is_active = models.BooleanField(
        verbose_name=u'是否启用',
        default=True,
        help_text=u'未启用的用户将无法登录系统. ',
    )
    is_super = models.BooleanField(
        verbose_name=u'超级管理员',
        default=False,
        help_text=u'超级管理员拥有最高权限，请谨慎授权 ',
    )
    last_login = models.DateTimeField(verbose_name=u'最后登录', blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', default=timezone.now)
    update_time = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)

    groups = models.ManyToManyField(
        'Group',
        verbose_name=u'用户所属组',
        blank=True,
        help_text=u'用户将拥有所有组的权限 ',
        related_name="user_set",
        related_query_name="user",
    )

    permissions = models.ManyToManyField(
        'Permission',
        verbose_name=u'用户权限',
        blank=True,
        help_text=u'用户拥有的所有权限',
        related_name="user_set",
        related_query_name="user",
    )

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    def set_password(self, password):
        self.password = hashers.make_password(password)
        self._password = password

    def check_password(self, raw_password):

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return hashers.check_password(raw_password, self.password, setter)

    objects = UserManager()

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户列表'


class PermissionManager(models.Manager):

    def get_by_code(self, code):
        return self.get(code=code)


class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name=u'权限名称', max_length=50)
    code = models.CharField(verbose_name=u'权限编码', unique=True, max_length=100)
    is_menu = models.BooleanField(verbose_name=u'是否为菜单', default=False)

    objects = PermissionManager()

    class Meta:
        verbose_name = u'权限资源'
        verbose_name_plural = u'权限资源列表'


class GroupManager(models.Manager):

    def get_by_name(self, name):
        return self.get(name=name)


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name=u'用户组标识', unique=True, max_length=20)
    title = models.CharField(verbose_name=u'用户组名称', max_length=20)
    permissions = models.ManyToManyField(
        'Permission',
        verbose_name=u'用户组权限列表',
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        verbose_name = u'用户组'
        verbose_name_plural = u'用户组列表'


class MenuManager(models.Manager):

    def get_by_name(self, name):
        return self.get(name=name)


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name=u'菜单名称', max_length=20)
    permissions = models.ManyToManyField(
        'Permission',
        verbose_name=u'菜单权限列表',
        blank=True,
    )

    objects = MenuManager()

    class Meta:
        verbose_name = u'菜单'
        verbose_name_plural = u'菜单列表'
