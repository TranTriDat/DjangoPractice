from django.contrib import admin
from .models import Category, Product, Image, Comment
from django.contrib import admin


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "category_name"]
    search_fields = ["id", "category_name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product_name"]
    search_fields = ["id", "product_name"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "comment", "product", "user", "created_date", "updated_date"]
    search_fields = ["id", "comment"]
    list_filter = ["comment", "product"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
