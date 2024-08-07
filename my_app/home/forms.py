from django import forms
from .models import *



class ContactForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('email_contact', 'firstname_contact' )




class SearchForm(forms.Form):
    q = forms.CharField(label='Search')




