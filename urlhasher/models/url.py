"""Model file for url."""
from django.db import models

class Url(models.Model):
    """model class for url"""
    long_url = models.URLField(blank=True)
    hash = models.CharField(max_length=64, unique=True)
    utm_source = models.CharField(max_length=50, blank=True, null=True)
    utm_medium = models.CharField(max_length=50, blank=True, null=True)
    utm_campaign = models.CharField(max_length=50, blank=True, null=True)
    clicks_remaining = models.IntegerField(default=100)
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return name of entity."""
        return self.long_url
