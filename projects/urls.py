from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectList.as_view()),
    path('project/<str:pk>/', views.PorjectDetails.as_view()),
    path('review/<str:pk>/', views.ReviewList.as_view()),
    path('tag/', views.TagList.as_view()),
]
