from django.contrib import admin
from .models import Comment, Review, Title, Category, Genre

admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
