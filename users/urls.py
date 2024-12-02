from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('authenticate/', UserViewSet.as_view({'get': 'authenticate', 'post': 'authenticate'}), name='authenticate'),
    path('profile/activate_invite_code/', ProfileViewSet.as_view({'get': 'activate_invite_code', 'post': 'activate_invite_code'}), name='activate_invite_code'),
]
