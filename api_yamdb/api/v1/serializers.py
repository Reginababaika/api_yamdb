from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Title, Genre, Category, Comment, Review
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, data):

        if self.initial_data['username'] == "me":
            raise serializers.ValidationError('Недопустимое имя пользователя')
        if User.objects.filter(username=self.initial_data['username']):
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        if User.objects.filter(email=self.initial_data['email']):
            raise serializers.ValidationError(
                'Пользователь с такой электронной почтой уже существует')
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',) 
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',) 
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='slug')
    genre = SlugRelatedField(queryset=Genre.objects.all(),
                             slug_field='slug',
                             many=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data 


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
