# Generated by Django 3.2.4 on 2021-07-15 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Почта'),
        ),
    ]
