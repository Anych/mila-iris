# Generated by Django 3.2.4 on 2021-06-25 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_alter_productfeatures_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=255, verbose_name='Номер заказа')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=255, verbose_name='Номер')),
                ('email', models.EmailField(max_length=255, verbose_name='Почта')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('country', models.CharField(max_length=255, verbose_name='Страна')),
                ('state', models.CharField(max_length=255, verbose_name='Область')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('order_note', models.TextField(blank=True, max_length=255, verbose_name='Примечания')),
                ('order_total', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Общая сумма')),
                ('delivery', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Стоимость доставки')),
                ('status', models.CharField(choices=[('Новый', 'Новый'), ('Подтверждён', 'Подтверждён'), ('Завершён', 'Завершён'), ('Отменён', 'Отменён')], default='Новый', max_length=255, verbose_name='Статус')),
                ('ip', models.CharField(blank=True, max_length=255, verbose_name='IP')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='В заказе')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Колличество')),
                ('product_price', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена продукта')),
                ('ordered', models.BooleanField(default=False, verbose_name='Заказан')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
                ('size', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.size', verbose_name='Размер')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ на продукт',
                'verbose_name_plural': 'Заказы на продукты',
            },
        ),
    ]
