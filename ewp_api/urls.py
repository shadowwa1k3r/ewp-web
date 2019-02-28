from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='auth-login'),
    path('council/list/', views.ListCouncilView.as_view(), name='council-all'),
    path('apartment/list/', views.ListApartmentAPIView.as_view(), name='apartment-all'),
    path('feedback/create/', views.FeedbackCreateView.as_view(), name='feedback-create'),
    path('fcmdevice/create/', views.FcmGetDeviceToken.as_view(), name='fcmid-create'),
]
