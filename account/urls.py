from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('main/', views.MainView.as_view(), name="main"),
    path('join/', views.JoinView.as_view(), name="join"),
    path('mydata/', views.MyDataView.as_view(), name="mydata"),
    path('alltable/', views.AllTableView.as_view(), name="alltable"),
    path('filedownload/', views.FileDownload.as_view(), name="filedownload"),
]