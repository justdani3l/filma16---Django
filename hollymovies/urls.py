"""
URL configuration for hollymovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from hollymovies import settings
from viewer.views import *

urlpatterns = [
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', SubmittablePasswordChangeView.as_view(),
         name='password_change'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('admin/', admin.site.urls),
    path('hello', hello),
    path('hello/<s>', hello_re),
    path('hello_encode', hello_encode),
    path('welcome/<s0>', welcome),
    path('home/<s0>', home),
    path('movies/', movies, name='index'),
    path('movies/<genre>', movies, name='index'),
    path('class', MoviesView.as_view(), name='class'),
    path('template', MoviesTemplateView.as_view(), name='template'),
    path('list/', MoviesListView.as_view(), name='list'),
    path('', MoviesCardView.as_view(), name='card'),
    path('category/<str:genre>', MoviesCardView.as_view(), name='card'),
    path('movie/<pk>/', MoviesDetailView.as_view(), name='movie_detail'),
    path('genre', GenreListView.as_view(), name='genre'),
    path('movie/create', MovieFormView.as_view(), name='movie_create'),
    path('movie/create_form', MovieCreateView.as_view(), name='movie_create_form'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>', MovieDeleteView.as_view(), name='movie_delete'),
    path('genre/create', GenreCreateView.as_view(), name='genre_create'),
    path('genre/update/<pk>', GenreUpdateView.as_view(), name='genre_update'),
    path('genre/delete/<pk>', GenreDeleteView.as_view(), name='genre_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)