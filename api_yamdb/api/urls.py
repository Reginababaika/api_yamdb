from django.urls import include, path
from rest_framework import routers
from .views import TitleViewSet, GenreViewSet, CategoryViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categiries', CategoryViewSet, basename='categiries')



urlpatterns = [
    path('', include(router.urls)),
]