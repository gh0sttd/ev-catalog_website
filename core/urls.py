from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from cars.views import add_to_compare, compare_view, index_view, catalog_view, car_detail_view, clear_compare_view, profile_view, test_drive_view, login_view, signup_view, logout_view, toggle_favorite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cars.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', index_view, name='home'), # Головна сторінка
    path('api/', include('cars.urls')),
    path('catalog/', catalog_view, name='catalog'),
    path('car/<int:pk>/', car_detail_view, name='car_detail'),
    path('compare/', compare_view, name='compare'),
    path('compare/add/<int:pk>/', add_to_compare, name='add_to_compare'),
    path('compare/clear/', clear_compare_view, name='clear_compare'),
    path('test-drive/<int:pk>/', test_drive_view, name='test_drive'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('favorite/<int:pk>/', toggle_favorite, name='toggle_favorite'),
    path('', lambda req: redirect('/catalog/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)