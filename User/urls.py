from django.urls import path, include
from .views import home, sigin, sigup, sigout, activate

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sigin', sigin, name='sigin'),
    path('sigup', sigup, name='sigup'),
    path('sigout', sigout, name='sigout'),

    path('activate/<uidb64>/<token>', activate, name='activate'),
]
