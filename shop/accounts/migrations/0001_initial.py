# Generated by Django 3.2.4 on 2021-06-16 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smartfields.fields
import smartfields.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name='Фамилия')),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='Имя')),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Почта')),
                ('phone_number', models.CharField(max_length=50, null=True, verbose_name='Номер телефона')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('confirm_email', models.BooleanField(default=False, verbose_name='Подтверждена почта')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Работник')),
                ('is_superadmin', models.BooleanField(default=False, verbose_name='Супер пользователь')),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('profile_picture', smartfields.fields.ImageField(blank=True, default='user_profile/default.png', upload_to='user_profile', verbose_name='Фото')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='Город')),
                ('state', models.CharField(blank=True, max_length=100, verbose_name='Область')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='Страна')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профайл',
                'verbose_name_plural': 'Профайлы',
            },
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
    ]
