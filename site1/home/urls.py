from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('destinations/', views.destinations_list, name='destinations'),
    path('destination/<int:id>/', views.destination_detail, name='destination_detail'),
    path('contact/', views.contact_view, name='contact'),
]
