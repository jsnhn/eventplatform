from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('events/', views.EventListView.as_view(), name='index'),
    path('events/<int:event_id>/', views.events_detail, name='detail'),
]