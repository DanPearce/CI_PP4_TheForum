"""
Forms used for the contact app.
"""
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Class to allow us to use the contact form
    """
    model = Contact
    fields = ('first_name', 'last_name', 'email', 'body')
