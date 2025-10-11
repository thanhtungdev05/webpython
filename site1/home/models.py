from django.db import models
from django.utils import timezone

class Destination(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)  # e.g. Biển, Núi, Văn hóa
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    featured = models.BooleanField(default=False)  # để hiện ở phần "featured"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        # trả về URL ảnh nếu có, ngược lại trả ảnh mẫu Unsplash
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # sample fallback (public unsplash link)
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=6b6f8f3d4a6c2c6cca2f8bd0df3f3fce"

class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.destination.name}"

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"
