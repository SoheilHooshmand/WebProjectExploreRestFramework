from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.ProfileList.as_view()),
    path('profile/<str:pk>/', views.ProfileDetails.as_view()),
    path('skills/', views.SkillList.as_view()),
    path('skills/<str:pk>/', views.SkillDetails.as_view()),
    path('messages/', views.MessageList.as_view()),
    path('messages/<str:pk>/', views.MessageDetails.as_view()),
]