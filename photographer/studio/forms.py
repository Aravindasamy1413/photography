from django import forms
from .models import Booking, FrameOrder

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


class FrameOrderForm(forms.ModelForm):
    class Meta:
        model = FrameOrder
        fields = '__all__'