from django.urls import include, path
from rest_framework import routers
from .views import get_token, get_signup, UserViewSet, TitleViewSet, ReviewViewSet
from .views import CommentViewSet, CategoryList, CategoryDetail, GenreList, GenreDetail

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', get_signup, name='get_signup'),
    path('auth/token/', get_token, name='get_token'),
    path('categories/', CategoryList.as_view()),
    path('categories/<slug:slug>/', CategoryDetail.as_view()),
    path('genres/', GenreList.as_view()),
    path('genres/<slug:slug>/', GenreDetail.as_view()),
]
