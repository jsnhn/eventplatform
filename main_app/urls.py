from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('events/', views.EventList.as_view(), name='index'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='detail'), #Primary Key directly aligns with Django's automatic handling of object
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
]