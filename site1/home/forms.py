from django import forms
from .models import Contact, Review

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min':1, 'max':5}),
            'comment': forms.Textarea(attrs={'rows':3}),
        }
