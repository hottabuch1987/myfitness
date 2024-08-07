from captcha.fields import ReCaptchaField
from django import forms
from .models import *



class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Feedback
        fields = ('email_contact', 'firstname_contact', 'text_contact', 'phone_contact', 'captcha')




class SearchForm(forms.Form):
    q = forms.CharField(label='Search')




