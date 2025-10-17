from django.contrib import admin
from .models import Destination, Tour, Booking, News, UserProfile
from datetime import date

# --- Destination ---
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'category', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'location')


# --- Tour ---
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'duration', 'featured')
    list_filter = ('destination', 'featured')
    search_fields = ('title', 'destination__name')
    actions = ['xoa_tour_het_han']

    # Hành động xóa tour hết hạn (nếu không có ngày kết thúc, xóa tour cũ hơn 30 ngày)
    def xoa_tour_het_han(self, request, queryset):
        from datetime import timedelta, date
        today = date.today()
        # Nếu model không có end_date, ta dùng ngày tạo để ước lượng
        het_han = queryset.filter(created_at__lt=today - timedelta(days=30))
        count = het_han.count()
        het_han.delete()
        self.message_user(request, f"🗑 Đã xóa {count} tour cũ hơn 30 ngày.")
    xoa_tour_het_han.short_description = "🗑 Xóa tour cũ (trên 30 ngày)"


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
