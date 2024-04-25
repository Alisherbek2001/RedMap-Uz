from django import forms

class Getimage(forms.Form):
    image = forms.ImageField()