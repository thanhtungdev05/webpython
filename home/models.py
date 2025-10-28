from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
class Destination(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Tên điểm đến")
    location = models.CharField(max_length=150, blank=True, verbose_name="Vị trí")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    category = models.CharField(max_length=50, blank=True, verbose_name="Phân loại")  # e.g. Biển, Núi, Văn hóa
    image = models.ImageField(upload_to='destinations/', null=True, blank=True, verbose_name="Ảnh đại diện")
    featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Điểm đến"
        verbose_name_plural = "Danh sách điểm đến"

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        """Trả về link ảnh, nếu không có thì dùng ảnh mặc định."""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop"


# 🚌 Tour du lịch
class Tour(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='tours',
        verbose_name="Điểm đến"
    )
    title = models.CharField(max_length=250, verbose_name="Tên tour")
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá (VNĐ)")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Thời lượng")
    schedule = models.TextField(blank=True, verbose_name="Lịch trình")
    image = models.ImageField(upload_to='tours/', null=True, blank=True, verbose_name="Ảnh tour")
    featured = models.BooleanField(default=False, verbose_name="Tour nổi bật")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tour du lịch"
        verbose_name_plural = "Danh sách tour"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        """Ưu tiên ảnh tour, nếu không có thì dùng ảnh điểm đến."""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return self.destination.image_url

    @property
    def average_rating(self):
        """Tính điểm trung bình từ các đánh giá."""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0



# ⭐ Đánh giá tour
class Review(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Tour"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Người dùng"
    )
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Số sao (1–5)")
    comment = models.TextField(blank=True, verbose_name="Nhận xét")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đánh giá"
        verbose_name_plural = "Danh sách đánh giá"
        unique_together = ('tour', 'user')  # Một user chỉ đánh giá 1 tour một lần

    def __str__(self):
        return f"{self.user.username} – {self.tour.title} ({self.rating}⭐)"

# 📋 Đơn đặt tour
class Booking(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    pax = models.PositiveSmallIntegerField(default=1)  # số lượng người
    booking_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending')  # Pending, Confirmed, Cancelled
    created_at = models.DateTimeField(auto_now_add=True)
     # Thông tin khách hàng bổ sung
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    cccd = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"Booking {self.id} - {self.full_name}"

    @property
    def total_price(self):
        if self.tour.price:
            return self.pax * self.tour.price
        return 0

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
