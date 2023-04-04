import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key in create.keys():
            with open('static/data/' + key, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    create[key](row)


def users(row):
    User.objects.create(id=row[0], username=row[1], email=row[2], role=row[3],
                        bio=row[4], first_name=row[5], last_name=row[6])


def category(row):
    Category.objects.create(id=row[0], name=row[1], slug=row[2])


def genre(row):
    Genre.objects.create(id=row[0], name=row[1], slug=row[2])


def titles(row):
    Title.objects.create(id=row[0], name=row[1], year=row[2],
                         category_id=row[3])


def review(row):
    Review.objects.create(id=row[0], title_id=row[1], text=row[2],
                          author_id=row[3], score=row[4], pub_date=row[5])


def comments(row):
    Comment.objects.create(id=row[0], review_id=row[1], text=row[2],
                           author_id=row[3], pub_date=row[4])


def genre_title(row):
    title = Title.objects.get(pk=row[1])
    genre = Genre.objects.get(pk=row[2])
    title.genre.add(genre)


create = {
    "users.csv": users,
    "category.csv": category,
    "genre.csv": genre,
    "titles.csv": titles,
    "review.csv": review,
    "comments.csv": comments,
    "genre_title.csv": genre_title,
}
