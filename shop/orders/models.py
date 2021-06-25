from django.db import models
from django.urls import reverse

from accounts.models import Account
from products.models import Product, Size


class Order(models.Model):
    """Model for order."""
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    STATUS = (
        ('Новый', 'Новый'),
        ('Подтверждён', 'Подтверждён'),
        ('Завершён', 'Завершён'),
        ('Отменён', 'Отменён'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    order_number = models.CharField(max_length=255, verbose_name='Номер заказа')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=255, verbose_name='Номер')
    email = models.EmailField(max_length=255, verbose_name='Почта')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    country = models.CharField(max_length=255, verbose_name='Страна')
    state = models.CharField(max_length=255, verbose_name='Область')
    city = models.CharField(max_length=255, verbose_name='Город')
    order_note = models.TextField(max_length=255, blank=True, verbose_name='Примечания')
    order_total = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Общая сумма')
    delivery = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Стоимость доставки')
    status = models.CharField(max_length=255, choices=STATUS, default='Новый', verbose_name='Статус')
    ip = models.CharField(max_length=255, blank=True, verbose_name='IP')
    is_ordered = models.BooleanField(default=False, verbose_name='В заказе')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def full_name(self):
        """Function return full name."""
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

    def get_order_url(self):
        return reverse('place_order', kwargs={'order_number': self.order_number})


class OrderProduct(models.Model):
    """Model for order products."""
    class Meta:
        verbose_name = 'Заказ на продукт'
        verbose_name_plural = 'Заказы на продукты'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    size = models.ForeignKey(Size, blank=True, on_delete=models.CASCADE, verbose_name='Размер')
    quantity = models.IntegerField(verbose_name='Колличество')
    product_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена продукта')
    ordered = models.BooleanField(default=False, verbose_name='Заказан')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return f'{self.product.article} - {self.product.category.name}: {self.product.brand}'

    def sub_total(self):
        return self.product.price * self.quantity
