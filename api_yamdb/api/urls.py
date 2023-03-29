from django.urls import include, path
from rest_framework import routers
from .views import get_token, get_signup, UserViewSet, TitleViewSet, GenreViewSet, CategoryViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categiries', CategoryViewSet, basename='categiries')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', get_signup, name='get_signup'),
    path('auth/token/', get_token, name='get_token'),
]
