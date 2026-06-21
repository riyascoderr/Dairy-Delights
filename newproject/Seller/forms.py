from django import forms
from .models import sellm, signins,logins
class sellf(forms.ModelForm):
    class Meta:
        model=sellm
        fields='__all__'
class signinf(forms.ModelForm):
    class Meta:
        model=signins
        fields=['seller_name', 'email', 'phone', 'location', 'gst_number']
class loginf(forms.ModelForm):
    class Meta:
        model=logins
        fields=['email']