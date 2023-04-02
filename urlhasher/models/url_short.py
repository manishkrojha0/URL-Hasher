"""Model file for url id."""
from django.db import models

class UrlShort(models.Model):
    """Model class for url id."""
    url = models.ForeignKey('Url', 
                              related_name="url_id", 
                              on_delete=models.DO_NOTHING, 
                              unique=True, 
                              null=False, 
                              blank=True
                              )
    value = models.CharField(null=True, max_length=12, unique=True)
        