from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, 'category')
router.register('products', views.ProductViewSet, 'product')
# router.register(r'images', views.ImageViewSet)
router.register('comments', views.CommentViewSet, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    # path('category', views.CategoryView.as_view(), name='list category api'),
    # path('products', views.ProductView.as_view(), name='list product api'),
    path('images/', views.ImageViewSet.as_view(), name='list image api'),
    path('total-comment/', views.AllComment.as_view(), name='list comment api'),
]
