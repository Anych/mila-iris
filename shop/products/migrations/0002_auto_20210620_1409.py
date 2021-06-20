# Generated by Django 3.2.4 on 2021-06-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=0, help_text='Поле высчитывается автоматически, можете написать цену в ручную', max_digits=10, null=True, verbose_name='Цена со скидкой'),
        ),
        migrations.AlterField(
            model_name='product',
            name='structure',
            field=models.CharField(blank=True, help_text='Например: Хлопок - 50%, полиэстер - 50%', max_length=255, null=True, verbose_name='Состав'),
        ),
    ]
