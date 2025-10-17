from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 🌐 Trang chính
    path('', views.home, name='home'),

    # 🏞 Tour
    path('tours/', views.tour_list, name='tour_list'),
    path('tour/<int:id>/', views.tour_detail, name='tour_detail'),
    path('destination/<int:dest_id>/', views.tour_from_destination, name='tour_from_destination'),

    # 🧾 Đặt tour
    path('booking/', views.booking_view, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),

    # 📰 Tin tức
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    # 👤 Người dùng
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update-pax/', views.update_pax, name='update_pax'),

    # ⚙️ AJAX cập nhật trạng thái
    path('profile/approve-booking/', views.approve_booking_ajax, name='approve_booking_ajax'),
    path('profile/cancel-booking/', views.cancel_booking_ajax, name='cancel_booking_ajax'),


    # 🧑‍💼 Admin duyệt / hủy (cho admin)
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # 📞 Giới thiệu & liên hệ
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ⚙️ API Gợi ý tìm kiếm
    path('suggest-destination/', views.suggest_destination, name='suggest_destination'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
