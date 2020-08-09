from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from . import views
urlpatterns = [
    path('register/', new_user_registration, name='sign-up'),
    # path('home/', home, name='home_page'),
    # path('login/', LoginView.as_view(), name='login_url'),
    # path('logout/', LogoutView.as_view(), name='logout_url'),
    # path('dashboard/', views.dashboardView, name='dashboard'),
    path('login/', login, name='login'),


]