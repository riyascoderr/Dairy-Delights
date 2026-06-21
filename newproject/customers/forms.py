from django import forms
from .models import signinm, loginm, buy
class signinf(forms.ModelForm):
    class Meta:
        model=signinm
        fields=['name', 'email', 'phone', 'address']
class loginf(forms.ModelForm):
    class Meta:
        model=loginm
        fields=['email']
class buyf(forms.ModelForm):
    class Meta:
        model=buy
        fields=['add', 'order', 'quantity']