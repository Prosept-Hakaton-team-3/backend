from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/',
         SpectacularSwaggerView.as_view(url_name='api/schema'),
         name='docs'),
    path('api/redoc/',
         SpectacularRedocView.as_view(url_name='api/schema'),
         name='redoc'),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
]
