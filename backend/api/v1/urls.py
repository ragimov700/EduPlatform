from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/register/',
         UserViewSet.as_view({'post': 'create'}),
         name='register'),
    path('', include(router.urls)),
]
