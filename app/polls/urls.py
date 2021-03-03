from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('longest_trips', views.longest_trips, name='longest_trips'),
]