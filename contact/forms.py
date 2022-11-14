"""
Forms used for the contact app.
"""
# Imports
# -----------------------------------------------------------------------
# Third Party
from django import forms
# Internal
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Class to allow us to use the contact form
    """
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'body')
