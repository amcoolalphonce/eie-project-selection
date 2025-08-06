# url patterns
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('select-projects/', views.select_projects, name='select_projects'),
]