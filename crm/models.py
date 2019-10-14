import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, _, send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_userid(self):
        prefix = 'best_'
        id_len = 8
        str_lst = [chr(ascii_code) for ascii_code in list(range(97, 123))+list(range(48, 58))]
        userid = prefix + ''.join(random.choices(str_lst, k=id_len))
        while UserProfile.objects.filter(userid=userid):
            userid = prefix + ''.join(random.choices(str_lst, k=id_len))
        return userid

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('用户名必须设置')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.userid = self.create_userid()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


# 1. 用户表
class UserProfile(AbstractBaseUser, PermissionsMixin):
    userid = models.CharField('用户ID', max_length=16, primary_key=True)
    username = models.EmailField('用户名', max_length=255, unique=True)
    password = models.CharField('密码', max_length=32)
    alias = models.CharField('昵称', max_length=64, null=True, blank=True)
    phone = models.CharField('手机号', max_length=32, null=True, blank=True)
    is_staff = models.BooleanField('是否职员', default=False)
    is_active = models.BooleanField('是否激活', default=True)
    is_admin = models.BooleanField('是否管理员', default=False)
    date_joined = models.DateTimeField('用户注册时间', auto_now_add=True)

    objects = UserManager()


    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)




