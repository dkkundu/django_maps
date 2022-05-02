"""Core > urls.py"""
# DJANGO URLS
from django.urls import path
# CORE IMPORTS
from Core import views

app_name = 'core'

urlpatterns = [
    # index url ---------------------------------------------------------------
    path('', views.IndexView.as_view(), name='index'),

    # user --------------------------------------------------------------------
    path(
        'users/', views.UserListView.as_view(), name='users'
    ),
    path(
        'user/create/', views.UserCreateView.as_view(), name='user_create'
    ),
    path(
        'user/detail/<int:pk>',
        views.UserDetailView.as_view(),
        name='user_detail'
    ),
    path(
        'user/update/<int:pk>',
        views.UserUpdateView.as_view(),
        name='user_update'
    ),
]
