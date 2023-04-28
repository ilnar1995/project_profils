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
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import RegisterUserForm, LoginUserForm, UserPasswordResetForm, RegisterUserCodeForm, EditUserProfileForm, \
    ResetEmailForm
from .models import User
from django.db import models
from django.contrib.auth import get_user_model
import random
from .tasks import send_code_mail


def verivicate_code(request, pk=None):
    if request.method == "POST":
        form = RegisterUserCodeForm(request.POST)
        if form.is_valid():
            user = get_user_model().objects.get(pk=pk)
            if user.code == form.data['code']:
                user.is_verified = True
                user.save()
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/registration_code.html', {'form': RegisterUserCodeForm(), 'pk': pk})

    else:
        form = RegisterUserCodeForm()
    return render(request, 'accounts/registration_code.html', {'form': form, 'pk': pk})


def reset_email_views(request, id=None):
    if request.method == "POST":
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            user = get_user_model().objects.get(id=id)
            code = random.randint(100000, 999999)
            user.code = code
            print(form.cleaned_data)
            user.email = form.cleaned_data['email']
            user.save()
            send_code_mail.delay(str(user.email), code)
            return redirect('registration_code', pk=user.pk)
    else:
        form = ResetEmailForm()
    return render(request, 'accounts/reset_email.html', {'form': form, 'id': id})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('registration_code')

    def form_valid(self,
                   form):  # переопределяем функ котор выпол-ся при успешном заполнении формы(для перехода по нежной ссылке при заплнении формы)
        # user = form.save()                                      #сохранить значения формы в БД (необязательно если не переопределяется функция form_valid)
        # login(self.request, user)                               #чтобы автоматический авторизоваля при валидном заплнении формы
        code = random.randint(100000, 999999)
        user = form.save()
        user.code = code
        user.save()
        send_code_mail.delay(str(user.email), code)
        return redirect('registration_code', pk=user.pk)  # переход при успеш заполнении формы


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):  # функция выхода из учетки
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm


def tessst(request):  # функция выхода из учетки
    print("dddddddddddddddddddddddddddddd")
    # movies = Movie.objects.all().prefetch_related(   #filter(url="tor-ljubov-i-grom")
    #     'actors'
    # )
    # for movie in movies:
    #     print(movie.actors.all(), "****")
    # print(movies.first().actors.all().first().name)
    str1 = ''
    for i in request.META:
        str1 = str1 + str(i) + "<br><br>"
    return HttpResponse(request.META["HTTP_USER_AGENT"])


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'account'
    template_name = 'accounts/account_detail.html'

    def get_object(self):
        return get_user_model().objects.get(id=self.kwargs['id'])


class UsersListView(ListView):
    model = User
    queryset = User.objects.all()
    template_name = 'accounts/account_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return get_user_model().objects.filter(is_verified=True)

    def get_context_data(self, **kwargs):  # функция для формирования и динамического и статического контекста
        context = super().get_context_data(**kwargs)  # через базовый класс ListView получам уже существующий контекст
        return context


class EditUserProfile(UpdateView):
    form_class = EditUserProfileForm
    template_name = 'accounts/edit_profile.html'

    # success_url = reverse_lazy('prifile')

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.kwargs['id'])

    def get_object(self):
        return get_user_model().objects.get(id=self.kwargs['id'])

    def form_valid(self,
                   form):  # переопределяем функ котор выпол-ся при успешном заполнении формы(для перехода по нежной ссылке при заплнении формы)
        # user = form.save()                                      #сохранить значения формы в БД (необязательно если не переопределяется функция form_valid)
        # login(self.request, user)                               #чтобы автоматический авторизоваля при валидном заплнении формы
        user = form.save()
        return redirect('prifile', id=user.id)
