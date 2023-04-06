from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=256,
        verbose_name='Название категории',)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
        verbose_name='Название жанра',)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


def validate_year(value):
    if value > date.today().year:
        raise ValidationError('Год выпуска не может быть больше текущего.')


class Title(models.Model):
    name = models.CharField(max_length=256,
        verbose_name='Название',)
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[validate_year],
        db_index=True,
    )
    rating = models.IntegerField(default=0,
        verbose_name='Рейтинг',)
    description = models.TextField(
        verbose_name='Описание',)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title,
        on_delete=models.CASCADE,
        verbose_name='Название',)
    genre = models.ForeignKey(Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр',)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField('Текст отзыва',)
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ]
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField('Текст комментария',)
