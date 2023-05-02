from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')

class DateInput(forms.DateInput):
    input_type = 'date'

class TripReviewForm(forms.ModelForm):
    # information about the object
    class Meta:
        model = Place
        # form has three fields
        fields = ('notes', 'date_visited', 'photo')
        widgets = {
            'date_visited': DateInput()
        }