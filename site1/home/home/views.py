from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Destination, Tour, Booking, News, UserProfile
from .forms import ContactForm, BookingForm, NewsForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour, News  # đổi lại đúng tên model của bạn
from .forms import UserRegisterForm, UserLoginForm
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.db.models import Q, F, Value
from django.db.models.functions import Abs
from django.db.models import Q, F, FloatField
from django.db.models.functions import Replace, Cast
# --- Trang chủ ---
def home(request):
    destinations = Destination.objects.filter(featured=True)[:6]
    tours = Tour.objects.filter(featured=True)[:6]
    news = News.objects.filter(is_published=True).order_by('-published_at')[:3]
    return render(request, 'index.html', {
        'destinations': destinations,
        'tours': tours,
        'news': news,})


def tour_list(request):
    q = request.GET.get('q', '').strip()
    destination = request.GET.get('destination', '').strip()
    city = request.GET.get('city', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    tours = Tour.objects.all()

    if q:
        tours = tours.filter(
            Q(title__icontains=q) |
            Q(destination__name__icontains=q) |
            Q(destination__location__icontains=q)
        )

    if destination:
        tours = tours.filter(destination__name__icontains=destination)
    if city:
        tours = tours.filter(destination__location__icontains=city)

    # Chuyển min/max price sang float nếu có
    try:
        if min_price:
            min_price_val = float(min_price.replace(',', '').strip())
            tours = tours.filter(price__gte=min_price_val)
        if max_price:
            max_price_val = float(max_price.replace(',', '').strip())
            tours = tours.filter(price__lte=max_price_val)
    except ValueError:
        pass

    return render(request, 'tour_list.html', {
        'tours': tours,
        'q': q,
        'destination': destination,
        'city': city,
        'min_price': min_price,
        'max_price': max_price
    })

# --- API gợi ý địa điểm khi gõ từ khóa ---
def suggest_destination(request):
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q:
        destinations = Destination.objects.filter(name__icontains=q).values_list('name', flat=True)[:5]
        suggestions = list(destinations)
    return JsonResponse(suggestions, safe=False)


# --- API gợi ý địa điểm khi gõ (autocomplete) ---
def suggest_destination(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = list(
            Destination.objects.filter(name__icontains=query)
            .values_list('name', flat=True)
            .distinct()[:5]
        )
    return JsonResponse(results, safe=False)



# --- Chi tiết tour ---
def tour_detail(request, id):
    tour = get_object_or_404(Tour, id=id)
    related_tours = Tour.objects.filter(destination=tour.destination).exclude(id=tour.id)[:3]
    return render(request, 'tour-detail.html', {'tour': tour, 'related_tours': related_tours})

# ... các import khác đã có

def tour_from_destination(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    tours = Tour.objects.filter(destination=destination)
    return render(request, 'tour-detail.html', {'destination': destination, 'tours': tours})


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
def tour_list(request):
    tours = Tour.objects.all()

    destination = request.GET.get('destination')
    city = request.GET.get('city')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if destination:
        tours = tours.filter(name__icontains=destination)
    if city:
        tours = tours.filter(city__icontains=city)
    if price_min:
        tours = tours.filter(price__gte=price_min)
    if price_max:
        tours = tours.filter(price__lte=price_max)
    if start_date:
        tours = tours.filter(start_date__gte=start_date)
    if end_date:
        tours = tours.filter(end_date__lte=end_date)

    return render(request, 'tour-list.html', {'tours': tours})
def suggest_destination(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = list(
            Destination.objects.filter(name__icontains=query)
            .values_list('name', flat=True)[:5]
        )
    return JsonResponse(results, safe=False)

def suggest_city(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = list(
            Tour.objects.filter(city__icontains=query)
            .values_list('city', flat=True)
            .distinct()[:5]
        )
    return JsonResponse(results, safe=False)
