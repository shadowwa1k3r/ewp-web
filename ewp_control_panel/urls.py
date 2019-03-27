from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('user/list/', views.UserListView.as_view(), name='userlist'),
    path('user/list/<int:pk>', views.UserDetailView.as_view(), name='user'),
    path('user/list/feedbacklist/<int:pk>', views.UserFeedbackList.as_view(), name='userfeedback'),
    path('feedback/list', views.FeedbackListView.as_view(), name='feedbacklist'),
    path('feedback/list/<int:pk>', views.FeedbackDetailView.as_view(), name='feedback'),
    path('api-key/', views.ApiKeyView.as_view(), name='apikey'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('push-notification/', views.PushNotificationView.as_view(), name='push'),
    path('council/list/', views.CouncilListView.as_view(), name='councillist'),
    path('council/list/<int:pk>', views.CouncilCreateView.as_view(), name='council'),
    path('streamaudio/group/list/<int:pk>/list/', views.AudioStreamListView.as_view(), name='audiolist'),
    path('streamaudio/group/list/', views.AudioStreamGroupListView.as_view(), name='audiogrouplist'),
    path('streamaudio/open/', views.StreamOpenView.as_view(), name='streamopen'),
    path('book/list/', views.BookListView.as_view(), name='booklist'),
]
