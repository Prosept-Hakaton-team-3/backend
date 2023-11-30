from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='docs'),
    path('redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
]
