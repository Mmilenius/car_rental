from django.contrib import admin
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users_cart/', views.UsersCartView.as_view(), name='users_cart'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('favorites/', views.user_favorites, name='favorites'),
    path('favorites/toggle/', views.toggle_favorite, name='toggle_favorite'),
]
