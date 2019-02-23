from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='auth-login'),
    path('council/list/', views.ListCouncilView.as_view(), name='council-all'),
    path('feedback/create/', views.FeedbackCreateView.as_view(), name='feedback-create')
]
