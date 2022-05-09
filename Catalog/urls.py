from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('category', views.all_categories, name='list-category'),
    path('product', views.all_products, name='list-product'),
    path('add_category', views.add_category, name='add-category'),
    path('add_product', views.add_product, name='add-product'),
    path('show_category/<category_id>', views.show_category, name='show-category'),
    path('show_product/<product_id>', views.show_product, name='show-product'),
    path('update_category/<category_id>', views.update_category, name='update-category'),
    path('update_product/<product_id>', views.update_product, name='update-product'),
    path('delete_product/<product_id>', views.delete_product, name='delete-product'),
    path('delete_category/<category_id>', views.delete_category, name='delete-category'),
]
