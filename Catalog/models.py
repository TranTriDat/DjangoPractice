from django.db import models
import sys

sys.path.insert(0, '/Practice1/practice1/User/')
from User.models import User


# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)
    category_name = models.CharField('Category Name', max_length=200)

    image = models.ImageField(null=True, blank=True, upload_to='category_images/')

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['category_name'], name="category_idx"),
            models.Index(fields=['image'], name="image_category_idx"),
        ]


class Product(models.Model):
    category = models.ManyToManyField(Category)
    product_name = models.CharField('Product Name', max_length=200)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['product_name'], name="product_idx")
        ]


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(null=True, blank=True, upload_to='product_images/')

    def __str__(self):
        return self.product.product_name + " image_list"

    class Meta:
        indexes = [
            models.Index(fields=['product'], name="product_image_idx"),
            models.Index(fields=['image'], name="image_product_idx"),
        ]


class Comment(models.Model):
    comment = models.CharField('Comment', null=True, max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-id']

