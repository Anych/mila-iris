# Generated by Django 3.2.4 on 2021-07-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Имя пользователя'),
        ),
    ]