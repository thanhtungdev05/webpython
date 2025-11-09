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
    path('booking/<int:tour_id>/', views.booking_view, name='booking_view'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('booking/<int:tour_id>/', views.booking_view, name='booking_view'),

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

    # 🧑‍💼 Admin duyệt / hủy
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # 💵 Thanh toán
    path('pay_cash/', views.pay_cash, name='pay_cash'),
    path('payment/qr/<int:booking_id>/', views.payment_qr, name='payment_qr'),
    path('booking/<int:pk>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('booking/<int:pk>/update-customer-info/', views.update_customer_info, name='update_customer_info'),
    # 📞 Giới thiệu & liên hệ
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Favorite tours
    path('favorite/add/<int:tour_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:tour_id>/', views.remove_favorite, name='remove_favorite'),
    


    # ⚙️ API Gợi ý tìm kiếm
    path('suggest-destination/', views.suggest_destination, name='suggest_destination'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)