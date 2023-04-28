
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Sum, Count, Q, Value, F, ExpressionWrapper, CharField, Case, When
from django.db.models.functions import Round, Concat, NullIf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView

from .IMDB import getMovieRating
# Create your views here.
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import ReviewForm, RatingForm, RatingReview
from .forms import RegisterUserForm, LoginUserForm, UserPasswordResetForm, RegisterUserCodeForm
from .models import Movie, Review, RatingMovie, IP_addres, LikeDislikeReview, Category
from django.db import models
from .utils1 import *
from django.contrib.auth import get_user_model
import random
from .tasks import send_code_mail



class HomeListView(PaginationMixin, ListView):
    model = Movie
    queryset = Movie.objects.all()
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.all().annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField())
        )

    def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
        c_def = self.get_user_context(**context)
        return c_def

class QuickSearchListView(PaginationMixin, ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = 'accounts/movie_search.html'
    context_object_name = 'movies'

    def get_queryset(self):
        a = ""
        if self.request.GET.get("q") != None:
            a = self.request.GET.get("q")
        return Movie.objects.filter(Q(name__icontains = a) | Q(tagline__icontains = a)).annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField())
        )
    def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
        c_def = self.get_user_context(**context)
        return c_def

class SearchListView(PaginationMixin, ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = 'accounts/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        filterargs = {}
        if self.request.GET.get("genre") != None:
            filterargs['genre__name'] = self.request.GET.get("genre")
        if self.request.GET.get("country") != None:
            filterargs['country'] = self.request.GET.get("country")
        if self.request.GET.get("my_range") != None:
            range_year = self.request.GET.get("my_range").split(';')
            filterargs['year__in'] = [i for i in range(int(range_year[0]), int(range_year[1])+1)]
        if self.request.GET.get("category") != None:
            filterargs['category__id__in'] = self.request.GET.getlist("category")
        #print(self.request.GET)
        return Movie.objects.filter(**filterargs).annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField())
        )
    def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
        c_def = self.get_user_context(**dict(list(context.items())+list(self.request.GET.items())))
        return c_def

class CategoryListView(PaginationMixin, ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = 'accounts/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs['cat_slug']).annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField())
        )

    def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
        c_def = self.get_user_context(**context)
        return c_def

class CategoryGenreListView(PaginationMixin, ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = 'accounts/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs['cat_slug'], genre__url=self.kwargs['genre_slug']).annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField())
        )

    def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
        c_def = self.get_user_context(**context)
        return c_def

class CategoryYearListView(PaginationMixin, ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = 'accounts/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs['cat_slug'], year=self.kwargs['year_int']).annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField())
        )

    def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
        c_def = self.get_user_context(**context)
        return c_def

class MovieDetailView(DetailMixin, DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'accounts/movie_detail.html'
    #pk_url_kwarg = 'pk'    #для pk
    slug_field = 'url'

    def get_queryset(self):
        return Movie.objects.filter(url = self.kwargs.get(self.slug_url_kwarg)).select_related(
            'translation', 'quality', 'category'
        ).annotate(
            full_name=ExpressionWrapper(Case(
                When(tagline=None, then=F('name')), default=Concat(F('name'), Value(': '), F('tagline'))), output_field=CharField()),
            like=Count('ratings__vote', filter=Q(ratings__vote=1)),
            dislike=Count('ratings__vote', filter=Q(ratings__vote=-1)),
            rat=Round(ExpressionWrapper(F('like') * 10.0 / NullIf(Count('ratings__vote'), 0), output_field=models.FloatField()), 1)   #NullIf чтобы не было деления на ноль на postgres
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = list(self.object.reviews.all().annotate(rating_review=Sum('likedislikereview__vote')).order_by(
            '-time_create').values())  # .filter(parent__isnull=True)
        context['reviews'] = self.coment(a)
        context["star_form"] = RatingForm()
        c_def = self.get_user_context(**context)
        return c_def

class AddReview(View):
    def post(self, request, pk):
        #print(request.POST.get('parent'))
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie_id = pk
            form.save()
        else:
            print('fail')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AddRaringMovie(DataMixin, View):
    def post(self, request):
        form = RatingForm(request.POST)
        ipp = self.get_client_ip(request)
        #print(request.POST, '-------------------')
        if form.is_valid():
            RatingMovie.objects.update_or_create(
                movie_id = int(request.POST.get('movie')),
                ip_id = ipp,
                defaults = {'vote':int(request.POST.get('vote'))}
            )
        else:
            return HttpResponse(status=400)

        return HttpResponse(status=200)

class AddLikeReview(DataMixin, View):
    def post(self, request):
        #print(request.POST)
        form = RatingReview(request.POST)
        ipp = self.get_client_ip(request)
        # print('-------------------')
        if form.is_valid():
            LikeDislikeReview.objects.update_or_create(
                Review_id=int(request.POST.get('Review')),
                ip_id=ipp,
                defaults={'vote': int(request.POST.get('vote'))}
            )
        else:
            return HttpResponse(status=400)

        return HttpResponse(status=200)




class RegisterUserCode(View):
    def post(self, request):
        form = RegisterUserCodeForm(request.POST)
        #print(request.POST, '-------------------')
        if form.is_valid():
            print(form.data['code'])
            form.save()
        else:
            return redirect('registration_code')

        return HttpResponse(status=200)
    def get(self, request):
        form = RegisterUserCodeForm()
        return render(request, 'accounts/registration_code.html', {"form":form})

def verivicate_code(request, pk=None):
   if request.method == "POST":
       form = RegisterUserCodeForm(request.POST)
       if form.is_valid():
           user = get_user_model().objects.get(pk=pk)
           if user.code == form.data['code']:
               login(request, user)
               return redirect('home')
           else:
               return render(request, 'accounts/registration_code.html', {'form':RegisterUserCodeForm(), 'pk': pk})

   else:
       form = RegisterUserCodeForm()
   return render(request, 'accounts/registration_code.html', {'form':form, 'pk': pk})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('registration_code')

    def form_valid(self, form):                                 #переопределяем функ котор выпол-ся при успешном заполнении формы(для перехода по нежной ссылке при заплнении формы)
        #user = form.save()                                      #сохранить значения формы в БД (необязательно если не переопределяется функция form_valid)
        #login(self.request, user)                               #чтобы автоматический авторизоваля при валидном заплнении формы
        code = random.randint(100000, 999999)
        user = form.save()
        user.code = code
        user.save()
        send_code_mail.delay(str(user.email), code)
        return redirect('registration_code', pk=user.pk)                                 #переход при успеш заполнении формы


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    # def get_context_data(self, object_list=None, **kwargs):     #функция для формирования и динамического и статического контекста
    #     context = super().get_context_data(**kwargs)            #через базовый класс ListView получам уже существующий контекст
    #     c_def = self.get_user_context(title='Авторизация') #создаем словарь с помощью функции из класса DataMixin (self нужен чтобы мы могли обращаться к методам базового класса)
    #     return dict(list(context.items())+list(c_def.items()))  #объединяем словари и возвращаем получ-ый словарь

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):                                       #функция выхода из учетки
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm



def tessst(request):                                       #функция выхода из учетки
    print("dddddddddddddddddddddddddddddd")
    #movies = Movie.objects.all().prefetch_related(   #filter(url="tor-ljubov-i-grom")
        #     'actors'
        # )
    # for movie in movies:
    #     print(movie.actors.all(), "****")
    #print(movies.first().actors.all().first().name)
    str1 = ''
    for i in request.META:
        str1 = str1 + str(i) + "<br><br>"
    return HttpResponse(request.META["HTTP_USER_AGENT"])