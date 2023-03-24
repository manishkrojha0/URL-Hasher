"""Manager file for urls."""
from urlhasher.models.url import Url

class UrlManager(object):
    """Class for url manager."""

    def __init__(self) -> None:
        pass

    def load_by_id(self, id):
        """Load url model by id."""
        try:
            url_obj = Url.objects.get(id=id)
        except Exception:
            url_obj = None
        
        return url_obj
    
    def load_by_long_url(self, long_url):
        """Load url object by long_url."""
        try:
            url_obj = Url.objects.get(long_url=long_url)
        except Exception:
            url_obj = None

        return url_obj
    
    def load_by_hash(self, hash):
        """Load by hash."""
        try:
            url_obj = Url.objects.get(hash=hash)
        except Exception:
            url_obj = None
        
        return url_obj

    
    def create(self, **kwargs):
        """Create entry in url table."""
        try:
            long_url = kwargs.get('long_url')
            utm_source = kwargs.get('utm_source')
            utm_medium = kwargs.get('utm_medium')
            utm_campaign = kwargs.get('utm_campaign')
            hash_value = kwargs.get('hash_value')
            url = Url(
                long_url=long_url,
                hash=hash_value,
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
            )
            url.save()
            return url
        except Exception:
            return None
