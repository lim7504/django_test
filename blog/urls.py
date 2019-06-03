from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('main/', views.MainView.as_view(), name="main"),
    path('second/', views.Second.as_view(), name="second"),
    path('filedownload/', views.FileDownload.as_view(), name="filedownload"),
]