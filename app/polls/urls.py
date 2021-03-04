from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('longest_trips', views.longest_trips, name='longest_trips'),
    path('update_vendor_id', views.update_vendor_id, name='update_vendor_id'),
]