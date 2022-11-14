"""
Views for the contact app
"""
import os
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import ContactForm


def contact(request):
    """
    View to render values related to the ContactForm
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            form = contact_form.save(commit=False)
            first_name = contact_form.cleaned_data['first_name']
            last_name = contact_form.cleaned_data['last_name']
            email = contact_form.cleaned_data['email']
            body = contact_form.cleaned_data['body']

            html = render_to_string('contact_form.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'body': body
            })

            email_from = os.environ.get('EMAIL_FROM')
            email_to = os.environ.get('EMAIL_TO')
            send_mail('theforum | New Contact Message', body,
                      email_from, [email_to], html_message=html)
            form.save()
            messages.success(request, 'Your message has been successfully' +
                             ' sent!')
            return redirect('home')
        else:
            contact_form = ContactForm()
            messages.error(request, 'There was an error sending your' +
                           ' message, please try again!')
    else:
        contact_form = ContactForm()
        context = {
            'contact_form': contact_form
        }

    return render(request, 'contact.html', context)
