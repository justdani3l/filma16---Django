from logging import getLogger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView, UpdateView, DeleteView

from viewer.forms import MovieForm, MovieModelForm, GenreModelForm, SignUpForm
from viewer.models import Movie, Genre
from viewer.permissions import StaffRequiredMixin

LOGGER = getLogger()


def hello(request):
    return HttpResponse('Hello, world!')


def hello_re(request, s):
    return HttpResponse(f'Hello, {s} world!')


def hello_encode(request):
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello, {s} world!')


def welcome(request, s0):
    s1 = request.GET.get('s1', '')
    return render(
        request, template_name='hello.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )


def home(request, s0):
    s1 = request.GET.get('s1', '')
    return render(
        request, template_name='home.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )


def movies(request, genre=None):
    rating = request.GET.get('rating', 0)
    if genre:
        movie = Movie.objects.filter(genre__name=genre).filter(rating__gt=rating)
    else:
        movie = Movie.objects.filter(rating__gt=rating)
    return render(
        request, template_name='home.html',
        context={'movies': enumerate(movie, start=1)}
    )


class MoviesView(View):
    def get(self, request):
        return render(
            request, template_name='all_movie.html',
            context={'movies': Movie.objects.all()}
        )


class MoviesTemplateView(TemplateView):
    template_name = 'all_movie.html'
    extra_context = {'movies': Movie.objects.all()}


class MoviesListView(ListView):
    template_name = 'list_movie.html'
    model = Movie


class MoviesCardView(ListView):
    template_name = 'card_movie.html'
    model = Movie

    def get_queryset(self):
        genre = self.kwargs.get('genre')
        queryset = super().get_queryset()
        if genre:
            return queryset.filter(genre__name=genre)
        return queryset


class MoviesDetailView(DetailView):
    template_name = 'detail_movie.html'
    model = Movie


class GenreListView(ListView):
    template_name = 'all_genre.html'
    model = Genre


class MovieFormView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description']
        )
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'new_form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('list')
    permission_required = 'viewer.create_movie'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'new_form.html'
    model = Movie
    form_class = MovieModelForm
    success_url = reverse_lazy('list')
    permission_required = 'viewer.change_movie'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a movie.')
        return super().form_invalid(form)


class MovieDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('list')
    permission_required = 'viewer.delete_movie'

    def test_func(self):
        return super().test_func() and self.request.user.is_superuser


class GenreCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'genre_form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('genre')
    permission_required = 'viewer.create_genre'


class GenreUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'genre_form.html'
    model = Genre
    form_class = GenreModelForm
    success_url = reverse_lazy('genre')
    permission_required = 'viewer.change_genre'


class GenreDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'genre_confirm_delete.html'
    model = Genre
    success_url = reverse_lazy('genre')
    permission_required = 'viewer.delete_genre'


class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('list')


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Assign the user to the "Basic Permission" group
        user = self.object
        basic_permission_group = Group.objects.get(name='Basic Permission')
        user.groups.add(basic_permission_group)

        # Set the user as active
        user.is_active = True
        user.save()

        return response
