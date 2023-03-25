from django.test import TestCase
from django.urls import reverse
import json
from urlhasher.managers.url_manager import UrlManager

class TestUrls(TestCase):
    """Test cases for URL_hashing."""
    def setUp(self) -> None:
        self.url = "http://127.0.0.1:8000/url-hasher/"
        self.payload = json.dumps({
            "long_url": "https://www.examples.com/",
            "utm_source": "test",
            "utm_medium": "test",
            "utm_campaign": "test"
        })
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.url_manager = UrlManager()
        return super().setUp()
    def test_successful_url_hashing(self):
        """Test for successfully url hashing."""
        response = self.client.post(self.url, data=self.payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('hashed_url', response.json())

    def test_click_url(self):
        # Test that a hashed URL can be clicked successfully
        data = json.loads(self.payload)
        long_url = data.get('long_url')
        url_obj = self.url_manager.load_by_long_url(long_url)
        if url_obj is None:
            self.assertFalse("failed url hashed.")
            hashed_url = None
        else:
            hashed_url = url_obj.hash
        response = self.client.get(reverse('hasher:click_url', args=[hashed_url]))
        self.assertEqual(response.status_code, 200)

    def test_privacy_click_url(self):
        # Test that a privacy hashed URL can be clicked successfully
        data = json.loads(self.payload)
        long_url = data.get('long_url')
        url_obj = self.url_manager.load_by_long_url(long_url)
        if url_obj is None:
            self.assertFalse("failed url hashed.")
            hashed_url = None
        else:
            hashed_url = url_obj.hash
        response = self.client.get(reverse('hasher:privacy_click_url', args=[hashed_url]))
        self.assertEqual(response.status_code, 200)

    def test_invalid_hashed_url(self):
        # Test that an invalid hashed URL returns a 404 error
        hashed_url = 'invalid_hash'
        response = self.client.get(reverse('hasher:click_url', args=[hashed_url]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_privacy_hashed_url(self):
        # Test that an invalid privacy hashed URL returns a 404 error
        hashed_url = 'invalid_hash'
        response = self.client.get(reverse('hasher:privacy_click_url', args=[hashed_url]))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_url(self):
        # Test that a nonexistent URL returns a 404 error
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)
