from django.urls import path, include
from .views import Home, SignIn, SignUp, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api-home', Home.as_view(), name='home-api'),
    path('signin', SignIn.as_view(), name='signin'),
    path('signup', SignUp.as_view(), name='signup'),
    path('', include(router.urls)),
]
