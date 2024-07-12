from .models import Room
from django.forms import ModelForm

class createform(ModelForm):
    class Meta:
        model= Room
        fields= ['topic', 'name', 'decription']















