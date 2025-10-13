from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # index.html
    path('tours/', views.tour_list, name='tour_list'),  # tour-list.html
    path('tour/<int:id>/', views.tour_detail, name='tour_detail'),  # tour-detail.html
    path('booking/', views.booking_view, name='booking'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('destination/<int:dest_id>/', views.tour_from_destination, name='tour_from_destination'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('news/', views.news_list, name='news_list'),
    



]
