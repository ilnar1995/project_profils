import django
from django.urls import path, include
from django.contrib.auth import views

from .views import RegisterUser, LoginUser, logout_user, \
    UserPasswordResetView, tessst, EditUserProfile, reset_email_views

from .views import verivicate_code, AccountDetailView, \
    UsersListView

urlpatterns = [
    path('', UsersListView.as_view(), name='home'),
    path('registrationcode/<int:pk>/', verivicate_code, name='registration_code'),
    path('reset_email/<slug:id>/', reset_email_views, name='reset_email'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path("accounts/password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/<slug:id>/', AccountDetailView.as_view(), name="prifile"),
    path('edit/<slug:id>/', EditUserProfile.as_view(), name="edit"),
]
