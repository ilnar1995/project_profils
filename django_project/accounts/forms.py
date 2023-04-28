from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordResetForm


#for email
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from .tasks import send_reset_mail
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model


#for email

class RegisterUserCodeForm(forms.Form):
    # vote = forms.IntegerField(widget=forms.RadioSelect())
    code = forms.CharField(max_length=6, min_length=6)

class ResetEmailForm(forms.Form):
    # vote = forms.IntegerField(widget=forms.RadioSelect())
    email = forms.EmailField(label='Почта')

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-input'}))  # переопределили стандартные атрибуты базового класса для изменения свойтва
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))  # переопределили стандартные атрибуты базового класса для изменения свойтва
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))  # переопределили стандартные атрибуты базового класса для изменения свойтва
    #captcha = CaptchaField(label='Введите символ с картинки')

    class Meta:  # class для расширения базового класса
        model = get_user_model()  # модель юзер это модель котор работает с таблицей auth_user
        fields = ('first_name', 'password1', 'password2',
                  'email')  # список полей котор надо отобразить в форме(если не вносить какой либо атрибут, данные не вносились в БД)

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class UserPasswordResetForm(PasswordResetForm):
    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        # subject = loader.render_to_string(subject_template_name, context)
        # # Email subject *must not* contain newlines
        # subject = "".join(subject.splitlines())
        # body = loader.render_to_string(email_template_name, context)

        # email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        # if html_email_template_name is not None:
        #     html_email = loader.render_to_string(html_email_template_name, context)
        #     email_message.attach_alternative(html_email, "text/html")

        del context['user']
        send_reset_mail.delay(
            subject_template_name,
            email_template_name, from_email, to_email, html_email_template_name, context
        )



class EditUserProfileForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-input'}))  # переопределили стандартные атрибуты базового класса для изменения свойтва
    last_name = forms.CharField(label='Фамилия', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))  # переопределили стандартные атрибуты базового класса для изменения свойтва
    birthday = forms.DateField(label='День рождения')  # переопределили стандартные атрибуты базового класса для изменения свойтва
    #captcha = CaptchaField(label='Введите символ с картинки')
    avatar = forms.ImageField(label='Фото')

    class Meta:  # class для расширения базового класса
        model = get_user_model()  # модель юзер это модель котор работает с таблицей auth_user
        fields = ('first_name', 'last_name', 'birthday',
                  'avatar')  # список полей котор надо отобразить в форме(если не вносить какой либо атрибут, данные не вносились в БД)