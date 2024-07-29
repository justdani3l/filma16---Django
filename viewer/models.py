from django.contrib.auth.models import User, Permission, Group
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=40, choices=[
        ("badge-primary", "Primary"),
        ("badge-secondary", "Secondary"),
        ("badge-success", "Success"),
        ("badge-danger", "Danger"),
        ("badge-warning", "Warning"),
        ("badge-info", "Info"),
        ("badge-light", "Light"),
        ("badge-dark", "Dark"),
    ],
        default='badge-primary'
    )

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=128)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()
    released = models.DateField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    trailer = models.URLField(blank=True)
    cover = models.ImageField(upload_to='movie_cover', blank=True, null=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField()


basic_permission_group, created = Group.objects.get_or_create(name='Basic Permission')
if created:
    # Define the permissions for Genre and Movie
    genre_permission = Permission.objects.get(codename='view_genre', content_type__app_label='viewer')
    movie_permission = Permission.objects.get(codename='view_movie', content_type__app_label='viewer')

    # Add the permissions to the group
    basic_permission_group.permissions.add(genre_permission, movie_permission)
    basic_permission_group.save()
