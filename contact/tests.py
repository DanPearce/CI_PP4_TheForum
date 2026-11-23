"""
Tests for the contact page. Run with:  SECRET_KEY=test python manage.py test
"""
from unittest import mock

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Contact

VALID = {'first_name': 'Ada', 'last_name': 'Lovelace', 'email': 'ada@example.com', 'body': 'Hello there'}


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ContactTests(TestCase):
    def test_page_loads(self):
        self.assertEqual(self.client.get(reverse('contact')).status_code, 200)

    @mock.patch.dict('os.environ', {'EMAIL_FROM': 'forum@example.com', 'EMAIL_TO': 'owner@example.com'})
    def test_valid_message_is_saved_and_emailed(self):
        response = self.client.post(reverse('contact'), VALID)
        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['owner@example.com'])

    def test_invalid_message_shows_the_page_again_and_sends_nothing(self):
        # regression: this used to crash with a server error
        response = self.client.post(reverse('contact'), dict(VALID, email='not-an-email'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
