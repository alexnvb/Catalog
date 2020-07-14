from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_urls(self):
        return reverse('catalog:product_list', args=[self.slug])


class Brand(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name

    def get_absolute_urls(self):
        return reverse('catalog:product_list', args=[self.category.slug, self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category',on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brand',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    avalible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('category', 'brand', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_urls(self):
        return reverse('catalog:product_detail', args=[self.category.slug, self.brand.slug, self.slug])