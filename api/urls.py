from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import  MessageView, UserProfileView, UserRegistrationView,\
    LoginView, UserProfileDetailView, LogoutView, UserMessageView, UserListView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('profile', UserProfileView.as_view(), name='user-profile'),
    path('users', UserListView.as_view(), name='user-list'),
    path('<str:username>/profile', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('message', MessageView.as_view(), name='message'),
    path('messages/<str:username>', UserMessageView.as_view(), name='message-view'),
    # path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    # path('direct-messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
    # path('notifications/', NotificationListView.as_view(), name='notification-list'),
]
