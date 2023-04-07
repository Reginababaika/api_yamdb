from django.urls import include, path
from rest_framework import routers
from .views import (get_token, signup, UserViewSet,
                    TitleViewSet, ReviewViewSet)
from .views import (CommentViewSet, CategoryViewSet,
                    GenreViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='get_token'),
]
