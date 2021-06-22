from datetime import datetime, timezone

from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from mptt.fields import TreeForeignKey

from smartfields import fields

from accounts.models import Account
from category.models import Category, Brand
from products.utils import gen_slug


class Product(models.Model):
    """Main model for products"""
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['category', 'price', '-create_date']

    article = models.CharField(max_length=255, verbose_name='Артикул')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Бренд')
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название модели')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', blank=True)
    structure = models.CharField(max_length=255, blank=True, null=True, verbose_name='Состав',
                                 help_text='Например: Хлопок - 50%, полиэстер - 50%')
    color = models.CharField(max_length=255, verbose_name='Цвет')
    another_color = models.ManyToManyField('self', blank=True, verbose_name='Другой цвет')
    made_in = models.CharField(max_length=255, verbose_name='Производство')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    is_discount = models.BooleanField(default=False, verbose_name='Скидка')
    discount_amount = models.IntegerField(blank=True, verbose_name='Размер скидки')
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,
                                         verbose_name='Цена со скидкой',
                                         help_text='Поле высчитывается автоматически, можете написать цену в ручную')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_recommend = models.BooleanField(default=False, verbose_name='Рекомендации')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.article}: {self.brand}'

    def product_image1(self):
        """First image in category_detail template"""
        image = ProductGallery.objects.filter(product=self).first()
        return image

    def product_image2(self):
        """Second image in category_detail template"""
        images = ProductGallery.objects.filter(product=self)
        image = images[1]
        return image

    def get_product_url(self):
        """URL for every product in site includes category, subcategory and own product's slug"""
        return reverse('product', kwargs={'category_slug': self.category.parent.slug,
                                          'subcategory_slug': self.category.slug, 'product_slug': self.slug})

    def average_review(self):
        """It is average rating for product"""
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def get_new_product(self):
        """Function for calculate if product is created in recent 30 days"""
        new = datetime.now(timezone.utc) - self.create_date
        if new.days <= 30:
            return new

    def count_review(self):
        """Function which calculate count of reviews for each product"""
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def calc_discount_price(self):
        """If product discount price is null, function calculate it automatically"""
        self.discount_price = int((int(self.price) * (100 - int(self.discount_amount))) / 100)
        return self.discount_price

    def you_save(self):
        """Function which calculate amount sum, which user save, if product has discount price"""
        if self.discount_price:
            return self.price - self.discount_price
        else:
            return self.price - self.calc_discount_price()

    def increment_views(self):
        """A simple function to calculate product views, which  I should to rewrite"""
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        """This function I added to automatically generate slug for each product"""
        if not self.slug:
            self.slug = gen_slug(self.category.name, self.brand.name)
        super().save(*args, **kwargs)


class ProductGallery(models.Model):
    """It is model for product images"""
    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    image = fields.ImageField(upload_to='products/product', verbose_name='Изображение')


class ProductFeatures(models.Model):
    """This is model for product additional information """
    class Meta:
        verbose_name = 'Дополниетельное поле продукта'
        verbose_name_plural = 'Дополниетельные поля продукта'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    key = models.CharField(max_length=255, verbose_name='Ключ')
    value = models.CharField(max_length=255, verbose_name='Значение')


class Size(models.Model):
    """This is model for product sizes"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    size = models.CharField(max_length=255, verbose_name='Размер')
    stock = models.IntegerField(default=1, verbose_name='Колличество')

    def __str__(self):
        return self.size


class ReviewRating(models.Model):
    """This is model for product reviews"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    review = models.TextField(max_length=1500, blank=True, verbose_name='Отзыв')
    rating = models.FloatField(verbose_name='Рейтинг')
    ip = models.CharField(max_length=255, blank=True, verbose_name='IP')
    status = models.BooleanField(default=True, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.review


class CustomerQuestion(models.Model):
    """This is model for product if customer has question about it"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    question = models.TextField(max_length=1500, blank=True, verbose_name='Вопрос')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    email = models.CharField(max_length=255, blank=True, verbose_name='Почта')
    name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.email
