from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from smartfields import fields


class MyAccountManager(BaseUserManager):
    """Account manager."""
    def create_user(self, first_name, last_name, email, password=None):
        """Creates and saves a new user."""
        if not email:
            raise ValueError('Введите e-mail')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            confirm_email=False,
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """Creates and saves a new super user."""
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """Custom user model that supports using email instead of username."""
    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['-date_joined']

    first_name = models.CharField(max_length=255, null=True, verbose_name='Фамилия')
    last_name = models.CharField(max_length=255, null=True, verbose_name='Имя')
    email = models.CharField(max_length=255, null=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=255, null=True, verbose_name='Номер телефона')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    confirm_email = models.BooleanField(default=False, verbose_name='Подтверждена почта')

    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    is_staff = models.BooleanField(default=False, verbose_name='Работник')
    is_superadmin = models.BooleanField(default=False, verbose_name='Супер пользователь')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    """Create the user profile to user."""
    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'

    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    profile_picture = fields.ImageField(blank=True,
                                        default='user_profile/default.png',
                                        upload_to='user_profile',
                                        verbose_name='Фото')
    city = models.CharField(max_length=255, blank=True, verbose_name='Город')
    state = models.CharField(max_length=255, blank=True, verbose_name='Область')
    country = models.CharField(max_length=255, blank=True, verbose_name='Страна')

    def __str__(self):
        return str(self.user)
