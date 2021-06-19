# Generated by Django 3.2.4 on 2021-06-19 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import smartfields.fields
import smartfields.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(max_length=255, verbose_name='Артикул')),
                ('model', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название модели')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='Слаг')),
                ('structure', models.CharField(blank=True, max_length=255, null=True, verbose_name='Состав')),
                ('color', models.CharField(max_length=255, verbose_name='Цвет')),
                ('made_in', models.CharField(max_length=255, verbose_name='Производство')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена')),
                ('is_discount', models.BooleanField(default=False, verbose_name='Скидка')),
                ('discount_amount', models.IntegerField(blank=True, verbose_name='Размер скидки')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=0, max_digits=10, verbose_name='Размер скидки')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_recommend', models.BooleanField(default=False, verbose_name='Рекомендации')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('another_color', models.ManyToManyField(blank=True, related_name='_products_product_another_color_+', to='products.Product', verbose_name='Другой цвет')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.brand', verbose_name='Бренд')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['category', 'price', '-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=255, verbose_name='Размер')),
                ('stock', models.IntegerField(default=1, verbose_name='Колличество')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, max_length=1500, verbose_name='Отзыв')),
                ('rating', models.FloatField(verbose_name='Рейтинг')),
                ('ip', models.CharField(blank=True, max_length=255, verbose_name='IP')),
                ('status', models.BooleanField(default=True, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', smartfields.fields.ImageField(upload_to='products/product', verbose_name='Изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галереи',
            },
            bases=(smartfields.models.SmartfieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='Ключ')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Дополниетелыное поле продукта',
                'verbose_name_plural': 'Дополниетелыные поля продукта',
            },
        ),
        migrations.CreateModel(
            name='CustomerQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, max_length=1500, verbose_name='Вопрос')),
                ('email', models.CharField(blank=True, max_length=255, verbose_name='Почта')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Имя')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
