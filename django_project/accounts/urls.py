import django
from django.urls import path, include
from django.contrib.auth import views

from .views import RegisterUser, LoginUser, logout_user, \
    UserPasswordResetView, tessst, RegisterUserCode

from .views import HomeListView, MovieDetailView, AddReview, AddRaringMovie, QuickSearchListView, AddLikeReview, \
    CategoryListView, CategoryGenreListView, CategoryYearListView, SearchListView, verivicate_code

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('quicksearch/', QuickSearchListView.as_view(), name='quicksearch'),
    path('search/', SearchListView.as_view(), name='search'),
    # path('<int:pk>/', MovieDetailView.as_view()),          #for pk
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('review_like/', AddLikeReview.as_view(), name='add_review_like'),
    path('rating_movie/', AddRaringMovie.as_view(), name='add_rating_movie'),
    path('category/<slug:cat_slug>/', CategoryListView.as_view(), name='category'),
    path('category/<slug:cat_slug>/<int:year_int>/', CategoryYearListView.as_view(), name='category_and_year'),
    path('category/<slug:cat_slug>/<slug:genre_slug>/', CategoryGenreListView.as_view(), name='category_and_genre'),
    path('test/', tessst, name='test'),
    path('registrationcode/<int:pk>/', verivicate_code, name='registration_code'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path("accounts/password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:slug>/', MovieDetailView.as_view()),
]
