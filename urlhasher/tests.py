from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string

from .models import HashedURL


class HashedURLTestCase(TestCase):
    def test_hash_url(self):
        # Test that a URL with query parameters can be hashed and saved to the database
        url = 'https://example.com/?utm_source=foo&utm_medium=bar'
        hashed_url = HashedURL.objects.hash_url(url)
        self.assertTrue(hashed_url.hash_value)
        self.assertEqual(hashed_url.original_url, url)

    def test_redirect_to_original_url(self):
        # Test that a hashed URL can be used to redirect to the original URL
        url = 'https://example.com/?utm_source=foo&utm_medium=bar'
        hashed_url = HashedURL.objects.hash_url(url)
        response = self.client.get(reverse('hashed_url', args=[hashed_url.hash_value]))
        self.assertRedirects(response, url, fetch_redirect_response=False)

    def test_hashed_url_single_use(self):
        # Test that a hashed URL can only be used once
        url = 'https://example.com/?utm_source=foo&utm_medium=bar'
        hashed_url = HashedURL.objects.hash_url(url)
        response1 = self.client.get(reverse('hashed_url', args=[hashed_url.hash_value]))
        response2 = self.client.get(reverse('hashed_url', args=[hashed_url.hash_value]))
        self.assertRedirects(response1, url, fetch_redirect_response=False)
        self.assertEqual(response2.status_code, 404)

    def test_hashed_url_privacy_aware(self):
        # Test that a hashed URL can be made privacy aware by adding a salt
        url = 'https://example.com/?utm_source=foo&utm_medium=bar'
        salt = get_random_string(length=10)
        hashed_url = HashedURL.objects.hash_url(url, salt=salt)
        response = self.client.get(reverse('hashed_url', args=[hashed_url.hash_value]))
        self.assertRedirects(response, url, fetch_redirect_response=False)
        self.assertNotIn(salt, response.url)
