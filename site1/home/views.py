from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Destination, Tour, Booking, News, UserProfile
from .forms import ContactForm, BookingForm, NewsForm
from django.shortcuts import render, get_object_or_404
from .models import Tour, News  # đổi lại đúng tên model của bạn
from .forms import UserRegisterForm, UserLoginForm
# --- Trang chủ ---
def home(request):
    destinations = Destination.objects.filter(featured=True)[:6]
    tours = Tour.objects.filter(featured=True)[:6]
    news = News.objects.filter(is_published=True).order_by('-published_at')[:3]
    return render(request, 'index.html', {'destinations': destinations, 'tours': tours, 'news': news})


# --- Danh sách tour ---
def tour_list(request):
    tours = Tour.objects.all().order_by('-created_at')
    return render(request, 'tour-list.html', {'tours': tours})


# --- Chi tiết tour ---
def tour_detail(request, id):
    tour = get_object_or_404(Tour, id=id)
    return render(request, 'tour-detail.html', {'tour': tour})


# --- Đặt tour ---
@login_required
def booking_view(request):
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        tour = get_object_or_404(Tour, id=tour_id)
        pax = int(request.POST.get('pax', 1))
        booking = Booking.objects.create(
            tour=tour,
            user=request.user,
            full_name=request.user.username,
            email=request.user.email,
            phone=request.user.profile.phone if hasattr(request.user, 'profile') else '',
            pax=pax,
            status='Pending'
        )
        messages.success(request, 'Đặt tour thành công! Vui lòng chờ xác nhận.')
        return redirect('profile')
    else:
        return redirect('tour_list')

def booking_success(request):
    return render(request, 'booking_success.html')

# --- Trang About / Contact ---
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# --- Danh sách tin tức ---
def news_list(request):
    news = News.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'news.html', {'news_list': news})


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug)
    return render(request, 'news-detail.html', {'news_item': item})


# --- Đăng ký ---
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data['phone'])
            messages.success(request, 'Tạo tài khoản thành công! Vui lòng đăng nhập.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# --- Đăng nhập ---
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Chào mừng {username} quay lại!')
                return redirect('home')
            else:
                messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu!')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# --- Đăng xuất ---
def user_logout(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công!')
    return redirect('home')


# --- Trang hồ sơ ---
@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'bookings': bookings})