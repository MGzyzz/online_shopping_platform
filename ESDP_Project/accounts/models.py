from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.IntegerField(verbose_name='Телефон')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    postal_code = models.CharField(max_length=100, verbose_name='Почтовый индекс')
    token = models.CharField(max_length=100, verbose_name='Токен', null=True, blank=True)
    shops = models.ManyToManyField('shop.Shop', related_name='shops', verbose_name='Магазины',
                                   through='shop.AccountShops')

