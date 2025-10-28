from django import forms
from .models import Booking, News, Booking, Tour
from .models import Booking, News
from .models import Booking
from .models import Booking
from .models import Booking
from .models import Booking
from .models import Booking
# (some duplicates removed intentionally; keep only the ones used below)

from .models import Booking, News
from .models import Booking

from .models import Booking

# Clean forms for contact & booking & review
from .models import Booking
from .models import Booking
# Simplify: define ContactForm, BookingForm, RegisterForm

from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':5}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'pax', 'booking_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'pax': forms.NumberInput(attrs={'class':'form-control', 'min':1}),
            'booking_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

from .models import News
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'summary', 'content', 'image', 'is_published']
# Form đăng ký người dùng
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']


# Form đăng nhập người dùng
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
