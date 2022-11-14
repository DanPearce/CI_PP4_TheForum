"""
View for the admin console for the contact app
"""
# Imports
# -----------------------------------------------------------------------
# Third Party
from django.contrib import admin
# Internal
from .models import Contact


@admin.register(Contact)
class ContactAdminView(admin.ModelAdmin):
    """
    A view that allows the admin console to view forms sent to the contact page
    """
    list_display = ('created_on', 'email', 'first_name', 'last_name')
    search_fields = ('body', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'first_name', 'last_name')
