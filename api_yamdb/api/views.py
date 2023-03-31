import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAdmin, IsAdminOrReadOnly
from reviews.models import Title, Genre, Category, User, Review
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from .serializers import SignupSerializer, TokenSerializer, UserSerializer
from .serializers import CommentSerializer, ReviewSerializer


class GenreList(generics.ListCreateAPIView):
    
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreDetail(generics.DestroyAPIView):
    
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)


class CategoryList(generics.ListCreateAPIView):
    
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDetail(generics.DestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(role = request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_signup(request):
    if User.objects.filter(
       username=request.data.get('username'), email=request.data.get('email')).exists():
        user = get_object_or_404(User, username=request.data.get('username'))
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {user.confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(User, username=request.data.get('username'))
        user.confirmation_code = random.randint(10000, 99999)
        user.save()
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {user.confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=request.data.get('username'))
        if not User.objects.filter(
       username=request.data.get('username')).exists():
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        if user.confirmation_code == request.data.get('confirmation_code'):
            refresh = RefreshToken.for_user(user)
            token = {'refresh': str(refresh),
                     'access': str(refresh.access_token)}
            return Response({'message': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdmin, )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


