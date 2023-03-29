from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Title, Genre, Category, User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, data):
        if data == "me":
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return data


class TokenSerializer(serializers.ModelSerializer):

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
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Category.objects.all(),
                                 slug_field='slug')
    genre = SlugRelatedField(queryset=Category.objects.all(),
                             slug_field='slug',
                             many=True)
    class Meta:
        fields = '__all__'
        model = Title
