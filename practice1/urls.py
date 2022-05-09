from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

import debug_toolbar

schema_view = get_schema_view(
    openapi.Info(
        title="Django Practice",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tridat123123@gmail.com"),
        license=openapi.License(name="Tran Tri Dat License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('User.urls')),
                  path('catalog/', include('Catalog.urls')),
                  path('user-api/', include('User.api.urls')),
                  path('catalog-api/', include('Catalog.api.urls')),
                  # path('', RedirectView.as_view(url='/Catalog/')),
                  path('social-auth/', include('social_django.urls', namespace='social')),
                  path('api-auth/', include('rest_framework.urls', namespace='rest')),
                  path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

                  path('__debug__/', include('debug_toolbar.urls')),

                  path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "My Django Practice"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome To The Admin Area"
