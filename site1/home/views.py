from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Destination, Tour, Booking, News, UserProfile
from .forms import ContactForm, BookingForm, NewsForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour, News, Favorite  # đổi lại đúng tên model của bạn
from .forms import UserRegisterForm, UserLoginForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django import template
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
import json
from django.http import JsonResponse
from .models import Tour
from django.views.decorators.csrf import csrf_exempt
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
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    tours = Tour.objects.select_related('destination').all()

    # --- Lọc theo từ khóa chung ---
    if q:
        tours = tours.filter(
            Q(title__icontains=q) |
            Q(destination__name__icontains=q) |
            Q(schedule__icontains=q)
        )

    # --- Lọc theo địa điểm ---
    if destination:
        tours = tours.filter(destination__name__icontains=destination)

    # --- Lọc theo thành phố ---
    if city:
        tours = tours.filter(destination__city__icontains=city)

    # --- Lọc theo giá ---
    if min_price:
        tours = tours.filter(price__gte=min_price)
    if max_price:
        tours = tours.filter(price__lte=max_price)

    # --- Lọc theo ngày ---
    if start_date:
        tours = tours.filter(start_date__gte=start_date)
    if end_date:
        tours = tours.filter(end_date__lte=end_date)

    # --- Gợi ý nếu không có kết quả ---
    similar_tours = None
    if not tours.exists() and (q or destination):
        similar_tours = Tour.objects.filter(featured=True)[:3]

    context = {
        'tours': tours,
        'similar_tours': similar_tours,
        'q': q,
        'destination': destination,
    }

    return render(request, 'tour-list.html', context)
# --- API gợi ý địa điểm khi gõ từ khóa ---
def suggest_destination(request):
    q = request.GET.get('q', '')
    if not q:
        return JsonResponse([], safe=False)
    suggestions = list(
        Destination.objects.filter(name__icontains=q)
        .values_list('name', flat=True)[:8]
    )
    return JsonResponse(suggestions, safe=False)






# --- Chi tiết tour ---
def tour_detail(request, id):
    tour = get_object_or_404(Tour, id=id)
    related_tours = Tour.objects.filter(destination=tour.destination).exclude(id=tour.id)[:3]

    # 🔹 Format giá tiền ở đây
    if tour.price is not None:
        tour.price = f"{tour.price:,.0f}".replace(",", ".")  # Ví dụ: 34.762.894
    else:
        tour.price = "Liên hệ"

    return render(request, 'tour-detail.html', {
        'tour': tour,
        'related_tours': related_tours
    })

# ... các import khác đã có

def tour_from_destination(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    tours = Tour.objects.filter(destination=destination)
    return render(request, 'tour-detail.html', {'destination': destination, 'tours': tours})


# --- Đặt tour ---
@login_required
def booking_view(request, tour_id):
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        tour = get_object_or_404(Tour, id=tour_id)
        pax = int(request.POST.get('pax', 1))

        booking = Booking.objects.create(
            tour=tour,
            user=request.user,
            full_name=request.user.get_full_name() or request.user.username,
            email=request.user.email,
            phone=getattr(request.user, 'phone', ''),
            pax=pax,
            status='Pending'
        )

        # ✅ Sau khi đặt tour, xóa tour khỏi yêu thích nếu có
        from .models import Favorite
        Favorite.objects.filter(user=request.user, tour=tour).delete()

        messages.success(request, f'Bạn đã đặt tour "{tour.title}" thành công!')
        return redirect('booking_success')
    
    return redirect('tour_list')


# --- Trang thông báo thành công ---
@login_required
def booking_success(request):
    return render(request, 'booking_success.html')

# --- Trang About / Contact ---
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# --- Danh sách tin tức ---
def news_list(request):
    news_list = News.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'news.html', {'news_list': news_list})

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news_detail.html', {'news': news})


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



def tour_list(request):
    tours = Tour.objects.all()

    # Lấy dữ liệu từ form
    query = request.GET.get('q') or request.GET.get('destination') or request.GET.get('city')
    destination = request.GET.get('destination')
    city = request.GET.get('city')
    duration = request.GET.get('duration')  # 👈 thêm dòng này
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Bộ lọc
    if destination:
        tours = tours.filter(destination__name__icontains=destination)
    if query:
        tours = tours.filter(destination__name__icontains=query)
    if city:
        tours = tours.filter(city__icontains=city)
    if duration:
        tours = tours.filter(duration__icontains=duration)  # 👈 lọc theo thời lượng
    if start_date:
        tours = tours.filter(start_date__gte=start_date)
    if end_date:
        tours = tours.filter(end_date__lte=end_date)

    # Format giá để hiển thị đẹp trong template
    for tour in tours:
        if tour.price is not None:
            tour.price = f"{tour.price:,.0f}".replace(",", ".")
        else:
            tour.price = "Liên hệ"

    return render(request, 'tour-list.html', {
        'tours': tours,
        'query': query,
        'destination': destination,
        'city': city,
        'duration': duration  # 👈 truyền thêm vào context (để hiển thị lại trong form nếu cần)
    })
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
@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    total_bookings = bookings.count()
    cancelled_bookings = bookings.filter(status='Hủy').count()
    completed_bookings = bookings.filter(status='Duyệt').count()

    # 🩶 Lấy danh sách tour yêu thích
    favorites = Favorite.objects.filter(user=request.user).select_related('tour')

    # ✅ Cập nhật số lượng pax (nếu có gửi POST)
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_pax = request.POST.get('pax')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        try:
            booking.pax = int(new_pax)
            booking.save()
        except ValueError:
            pass

    context = {
        'bookings': bookings,
        'favorites': favorites,
        'total_bookings': total_bookings,
        'cancelled_bookings': cancelled_bookings,
        'completed_bookings': completed_bookings,
    }

    if request.user.is_staff:
        context['admin_bookings'] = Booking.objects.all().order_by('-created_at')

    return render(request, 'profile.html', context)


# -----------------------
# 💰 Cập nhật số lượng khách
# -----------------------
@login_required
def update_pax(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        pax = request.POST.get('pax')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        try:
            booking.pax = int(pax)
            booking.save()
            total_price = booking.total_price
            total_price_formatted = f"{total_price:,.0f} ₫"
            return JsonResponse({'success': True, 'total_price': total_price_formatted})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Giá trị không hợp lệ'})
    return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'})

# -----------------------
# 🟢 AJAX: Duyệt đơn (cho user)
# -----------------------
@login_required
def approve_booking_ajax(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.status = 'Duyệt'
        booking.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'})

# -----------------------
# 🔴 AJAX: Hủy đơn (cho user)
# -----------------------
@login_required
@csrf_exempt
def cancel_booking_ajax(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.status = "Hủy"
            booking.save()
            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Không tìm thấy đơn đặt!"})
    return JsonResponse({"success": False, "error": "Yêu cầu không hợp lệ."})
# 💵 Thanh toán tiền mặt
def pay_cash(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        if booking.status == "Duyệt":
            booking.status = "Đã thanh toán"
            booking.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Chỉ có thể thanh toán tour đã duyệt!"})
    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ."})

# 💳 Cổng thanh toán QR (giả lập)
def payment_qr(request, booking_id):
    amount = request.GET.get("amount", 0)
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "payment_qr.html", {"booking": booking, "amount": amount})

# -----------------------
# 🧑‍💼 Dành cho Admin
# -----------------------
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@admin_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Duyệt'
    booking.save()
    return redirect('profile')

@admin_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Hủy'
    booking.save()
    return redirect('profile')
@login_required
@csrf_exempt
def pay_cash(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.status = "Đã thanh toán"
            booking.save()
            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Không tìm thấy đơn đặt tour."})
    return JsonResponse({"success": False, "error": "Yêu cầu không hợp lệ."})


@login_required
@csrf_exempt
def cancel_booking_ajax(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.status = "Hủy"
            booking.save()
            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Không tìm thấy đơn đặt tour."})
    return JsonResponse({"success": False, "error": "Yêu cầu không hợp lệ."})
@csrf_exempt
def update_booking_status(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        status = data.get("status")  # "Đã thanh toán"
        booking = Booking.objects.get(pk=pk)
        booking.status = status
        booking.save()

        # URL profile
        profile_url = request.build_absolute_uri(reverse('profile'))

        # Render email HTML
        html_content = render_to_string('emails/payment_confirmation.html', {
            'user': booking.user,
            'booking': booking,
            'profile_url': profile_url,
            'year': datetime.now().year
        })
        text_content = strip_tags(html_content)

        # Gửi email
        email = EmailMessage(
            subject=f"Xác nhận thanh toán Tour #{booking.id}",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.user.email]
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)

        return JsonResponse({"success": True, "status": booking.status})
    return JsonResponse({"success": False})
@csrf_exempt
def update_customer_info(request, pk):
    if request.method == "POST":
        booking = Booking.objects.get(pk=pk)
        data = json.loads(request.body)
        booking.full_name = data.get("full_name")
        booking.phone = data.get("phone")
        booking.email = data.get("email")
        booking.address = data.get("address")
        booking.birth_date = data.get("birth_date")
        booking.cccd = data.get("cccd")
        booking.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
# ==========================
# ❤️ Thêm tour vào yêu thích
# ==========================
@login_required
def add_favorite(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    Favorite.objects.get_or_create(user=request.user, tour=tour)
    messages.success(request, f'Đã thêm "{tour.title}" vào danh sách yêu thích!')
    
    # ✅ Chuyển đến trang Tour Yêu Thích
    return redirect('profile')


# ==========================
# 💔 Xóa tour khỏi yêu thích
# ==========================
@login_required
def remove_favorite(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    Favorite.objects.filter(user=request.user, tour=tour).delete()
    messages.info(request, f'Đã xóa "{tour.title}" khỏi danh sách yêu thích.')
    return redirect('profile')

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("message", "").lower().strip()

        # ======== IMPORT MODELS =========
        from .models import Tour, Destination

        # =================================================
        # 1. GỢI Ý TOUR NỔI BẬT
        # =================================================
        if "tour" in question and ("gợi ý" in question or "tư vấn" in question or "đề xuất" in question):
            tours = Tour.objects.filter(featured=True)[:5]

            if not tours.exists():
                return JsonResponse({"reply": "Hiện chưa có tour nổi bật nào."})

            reply = "Dưới đây là các tour nổi bật của chúng tôi:<br>"
            for t in tours:
                reply += f"👉 <a href='/tour/{t.id}/'>{t.title}</a><br>"

            reply += "<br>Bạn muốn tìm tour nào ạ?"
            return JsonResponse({"reply": reply})

        # =================================================
        # 2. TÌM TOUR THEO ĐIỂM ĐẾN
        # =================================================
        for dest in Destination.objects.all():
            if dest.name.lower() in question:
                tours = Tour.objects.filter(destination=dest)

                if not tours.exists():
                    return JsonResponse({"reply": f"Hiện chưa có tour nào đến {dest.name}."})

                reply = f"Các tour đến <b>{dest.name}</b>:<br>"
                for t in tours:
                    reply += f"👉 <a href='/tour/{t.id}/'>{t.title}</a><br>"

                reply += "<br>Bạn muốn xem chi tiết tour nào?"
                return JsonResponse({"reply": reply})

        # =================================================
        # 3. TÌM TOUR THEO TÊN TOUR
        # =================================================
        for tour in Tour.objects.all():
            if tour.title.lower() in question or any(word in question for word in tour.title.lower().split()):

                # --- Hỏi giá ---
                if "giá" in question:
                    price = f"{tour.price:,}" if tour.price else "Đang cập nhật"
                    return JsonResponse({
                        "reply": f"Giá của tour <b>{tour.title}</b> là <b>{price} VNĐ</b>.<br>"
                                 f"👉 <a href='/tour/{tour.id}/'>Xem chi tiết tour</a>"
                    })

                # --- Hỏi lịch trình ---
                if "lịch trình" in question or "schedule" in question:
                    return JsonResponse({
                        "reply": f"Lịch trình của tour <b>{tour.title}</b>:<br>{tour.schedule[:500]}..."
                                 f"<br><br>👉 <a href='/tour/{tour.id}/'>Xem đầy đủ</a>"
                    })

                # --- Hỏi thời tiết ---
                if "thời tiết" in question or "mưa" in question or "nắng" in question:
                    return JsonResponse({
                        "reply": f"Bạn muốn hỏi thời tiết tại <b>{tour.destination.name}</b> ạ?<br>"
                                 f"Hiện tại thời tiết ổn định, tùy mùa sẽ thay đổi nhẹ.<br>"
                                 f"👉 <a href='/tour/{tour.id}/'>Xem tour</a>"
                    })

                # --- Hỏi cách đặt tour ---
                if "đặt tour" in question or "cách đặt" in question:
                    return JsonResponse({
                        "reply": (
                            f"Hướng dẫn đặt tour <b>{tour.title}</b>:<br>"
                            "1️⃣ Truy cập trang chi tiết tour<br>"
                            "2️⃣ Nhấn nút <b>Đặt ngay</b><br>"
                            "3️⃣ Nhập thông tin của bạn<br>"
                            "4️⃣ Chọn phương thức thanh toán<br>"
                            "5️⃣ Xác nhận đặt tour 🎉<br><br>"
                            f"👉 <a href='/tour/{tour.id}/'>Đi tới trang đặt tour</a>"
                        )
                    })

                return JsonResponse({
                    "reply": f"Bạn muốn xem thông tin gì về tour <b>{tour.title}</b>?<br>"
                             "- Giá tour<br>"
                             "- Lịch trình<br>"
                             "- Thời tiết<br>"
                             "- Hướng dẫn đặt tour<br>"
                })

        # =================================================
        # 4. TOUR TRONG NƯỚC / NGOÀI NƯỚC
        # =================================================
        if "trong nước" in question or "tour trong nước" in question:
            tours = Tour.objects.filter(tour_type__in=["domestic", "trong nuoc", "trong_nuoc", "trong-nuoc"])
            reply = "Các tour trong nước:<br>"
            for t in tours:
                reply += f"👉 <a href='/tour/{t.id}/'>{t.title}</a><br>"
            return JsonResponse({"reply": reply})


        if "ngoài nước" in question or "nước ngoài" in question or "tour nước ngoài" in question:
            tours = Tour.objects.filter(tour_type__in=["foreign", "ngoai nuoc", "ngoai_nuoc", "ngoai-nuoc"])
            reply = "Các tour nước ngoài:<br>"
            for t in tours:
                reply += f"👉 <a href='/tour/{t.id}/'>{t.title}</a><br>"
            return JsonResponse({"reply": reply})

        # =================================================
        # 5. HƯỚNG DẪN ĐẶT TOUR – CHUNG
        # =================================================
        if "đặt tour" in question or "cách đặt" in question:
            reply = (
                "Để đặt tour, bạn thực hiện các bước sau:<br>"
                "1️⃣ Chọn tour bạn muốn<br>"
                "2️⃣ Nhấn nút <b>Đặt tour</b><br>"
                "3️⃣ Nhập thông tin cá nhân<br>"
                "4️⃣ Chọn hình thức thanh toán<br>"
                "5️⃣ Xác nhận đặt tour thành công 🎉<br><br>"
                "Bạn muốn đặt tour nào ạ?"
            )
            return JsonResponse({"reply": reply})

        # =================================================
        # 6. HƯỚNG DẪN THANH TOÁN – CHUNG
        # =================================================
        if "thanh toán" in question or "momo" in question or "chuyển khoản" in question or "visa" in question:
            reply = (
                "Hiện tại hệ thống hỗ trợ 3 hình thức thanh toán:<br><br>"
                "<b>💜 1. Thanh toán bằng Momo</b><br>"
                "• Quét mã QR<br>"
                "• Hoặc nhập số điện thoại Momo<br><br>"

                "<b>🏦 2. Chuyển khoản ngân hàng</b><br>"
                "• Chuyển khoản theo thông tin hiển thị<br>"
                "• Nội dung: Tên + Mã tour<br><br>"

                "<b>💳 3. Thanh toán bằng Visa/MasterCard</b><br>"
                "• Nhập số thẻ, ngày hết hạn, mã CVV<br><br>"

                "Bạn muốn thanh toán bằng phương thức nào?"
            )
            return JsonResponse({"reply": reply})

        # =================================================
        # 7. LỜI CHÀO
        # =================================================
        if "hello" in question or "xin chào" in question or "hi" in question:
            return JsonResponse({
                "reply": (
                    "Xin chào! Tôi là TravelBot 🤖<br>"
                    "Tôi có thể giúp bạn tìm tour, xem giá, lịch trình, thời tiết "
                    "và hướng dẫn đặt tour – thanh toán."
                )
            })

        # =================================================
        # 8. KHÔNG HIỂU
        # =================================================
        return JsonResponse({
            "reply": (
                "Mình chưa hiểu câu hỏi của bạn 😅<br>"
                "Bạn có thể hỏi về:<br>"
                "- Gợi ý tour<br>"
                "- Giá tour<br>"
                "- Lịch trình<br>"
                "- Cách đặt tour<br>"
                "- Thanh toán<br>"
                "- Tour trong nước / nước ngoài"
            )
        })

    return JsonResponse({"error": "Invalid request"})










