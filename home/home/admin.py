from django.contrib import admin
from .models import Destination, Tour, Booking, News, UserProfile

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'category', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'location')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'duration', 'featured')
    list_filter = ('destination', 'featured')
    search_fields = ('title', 'destination__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'tour', 'pax', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
