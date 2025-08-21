from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('select_projects/', views.select_projects, name='select_projects'),
    path('my_projects/', views.user_selected_projects, name='my_projects'),
]