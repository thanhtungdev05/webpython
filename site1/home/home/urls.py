from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # nếu file này là home/urls.py

urlpatterns = [
    path('', views.home, name='home'),  # index.html
    path('tours/', views.tour_list, name='tour_list'),  # tour-list.html
    path('tour/<int:id>/', views.tour_detail, name='tour_detail'),  # tour-detail.html
    path('booking/', views.booking_view, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Tin tức
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    # Người dùng
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Tour theo điểm đến
    path('destination/<int:dest_id>/', views.tour_from_destination, name='tour_from_destination'),

    # API gợi ý
    path('api/suggest-destination/', views.suggest_destination, name='api_suggest_destination'),
    path('suggest-destination/', views.suggest_destination, name='suggest_destination'),


]


