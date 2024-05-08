from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', blank=False)
    price = models.IntegerField(verbose_name='Цена', blank=False)
    image = models.ImageField(upload_to='product_images', verbose_name='Изображение товара', blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', blank=False)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})
