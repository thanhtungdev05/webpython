from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Destination
from .forms import ContactForm, ReviewForm

def home(request):
    featured = Destination.objects.filter(featured=True).order_by('-created_at')[:6]
    if not featured.exists():
        featured = Destination.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'featured_destinations': featured})

def destinations_list(request):
    q = request.GET.get('q', '')
    qs = Destination.objects.all().order_by('-created_at')
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(location__icontains=q)
    return render(request, 'destinations.html', {'destinations': qs})

def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.destination = destination
            rev.save()
            messages.success(request, "Cảm ơn bạn đã gửi đánh giá!")
            return redirect(reverse('destination_detail', args=[destination.id]))
    else:
        form = ReviewForm()
    reviews = destination.reviews.all().order_by('-created_at')
    return render(request, 'tour_detail.html', {'destination': destination, 'form': form, 'reviews': reviews})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cảm ơn! Chúng tôi sẽ liên hệ lại sớm.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
