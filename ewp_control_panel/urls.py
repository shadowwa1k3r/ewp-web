from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='userlist'),
    path('api-key/', views.ApiKeyView.as_view(), name='apikey'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
