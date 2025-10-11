from django.contrib import admin
from .models import Destination, Review, Contact

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'category', 'price', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'location')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'destination', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user_name', 'destination__name')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'processed')
    list_filter = ('processed',)
    search_fields = ('name', 'email')
