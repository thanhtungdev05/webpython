from django.contrib import admin
from .models import Destination, Tour, Booking, News, UserProfile
from datetime import date, timedelta

# --- Destination ---
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'category', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'location')


# --- Tour ---
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'destination', 'price_display', 'duration', 'featured', 'created_at')
    list_filter = ('destination', 'featured')
    search_fields = ('title', 'destination__name')
    actions = ['xoa_tour_het_han', 'xoa_tour_loi_hinhanh']

    # --- Hiển thị giá tiền đẹp hơn ---
    def price_display(self, obj):
        return f"{obj.price:,.0f} ₫"
    price_display.short_description = "Giá Tour"

    # --- Hành động xóa tour cũ (trên 30 ngày) ---
    def xoa_tour_het_han(self, request, queryset):
        today = date.today()
        het_han = queryset.filter(created_at__lt=today - timedelta(days=30))
        count = het_han.count()
        het_han.delete()
        self.message_user(request, f"🗑 Đã xóa {count} tour cũ hơn 30 ngày.")
    xoa_tour_het_han.short_description = "🗑 Xóa tour cũ (trên 30 ngày)"

    # --- Hành động xóa tour lỗi hình ảnh ---
    def xoa_tour_loi_hinhanh(self, request, queryset):
        loi = queryset.filter(image__isnull=True) | queryset.filter(image='')
        count = loi.count()
        loi.delete()
        self.message_user(request, f"🚫 Đã xóa {count} tour lỗi hình ảnh (thiếu ảnh).")
    xoa_tour_loi_hinhanh.short_description = "🚫 Xóa tour lỗi hình ảnh"


# --- Booking ---
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'tour', 'pax', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email')
    actions = ['duyet_don', 'huy_don']

    # Duyệt đơn
    def duyet_don(self, request, queryset):
        count = queryset.update(status='Duyệt')
        self.message_user(request, f"✅ Đã duyệt {count} đơn thành công.")
    duyet_don.short_description = "✅ Duyệt đơn đã chọn"

    # Hủy đơn
    def huy_don(self, request, queryset):
        count = queryset.update(status='Hủy')
        self.message_user(request, f"❌ Đã hủy {count} đơn thành công.")
    huy_don.short_description = "❌ Hủy đơn đã chọn"


# --- News ---
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    prepopulated_fields = {"slug": ("title",)}


# --- UserProfile ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
