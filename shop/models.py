from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=10,
                                decimal_places=2)
    stock = models.IntegerField('Количество на складе',
                                default=0)
    description = models.TextField('Описание',
                                   blank=True)
    image_url = models.URLField('URL изображения',
                                blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    customer_name = models.CharField('Имя покупателя', max_length=100)
    customer_email = models.EmailField('Email')
    customer_phone = models.CharField('Телефон', max_length=20)
    customer_address = models.TextField('Адрес доставки')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField('Сумма заказа', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f'Заказ #{self.id} - {self.customer_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'