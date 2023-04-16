"""Manager file for url short model."""
from urlhasher.models.url_short import UrlShort
from urlhasher.models.url import Url
import random, string

class UrlShortManager(object):
    """class for url short model."""

    def __init__(self) -> None:
        """Init method."""
        pass

    def load_by_url_id(self, url_id):
        """Load url short by url id."""
        try:
            url_short_obj = UrlShort.objects.get(url_id=url_id)
        except UrlShort.DoesNotExist:
            url_short_obj = None
        
        return url_short_obj
    
    def load_by_value(self, value):
        """Load url short by value."""
        try:
            url_short_obj = UrlShort.objects.get(value=value)
        except UrlShort.DoesNotExist:
            url_short_obj = None
        
        return url_short_obj
    
    def load_value_by_hash(self, url_hash):
        """Load url short value by url hash."""
        try:
            url_obj = Url.objects.get(hash=url_hash)
            url_short_obj = self.load_by_url_id(url_obj.id) if url_obj else None
        except Exception:
            url_short_obj = None
        
        return url_short_obj
    
    def create_url_short(self, hash):
        """Create url short value."""
        try:
            url_obj = Url.objects.get(hash=hash)
            value = self.generate_random_string()
            url_short_obj = UrlShort.objects.filter(url = url_obj)
            # if url_short_obj:
            #     return url_short_obj[0]
            # else:
            url_short_obj = UrlShort.objects.create(url_id=url_obj.id, value=value)
        except Exception as e:
            print(e)
            return None
        
        return url_short_obj

    def generate_random_string(self, size=8, chars=string.ascii_lowercase + string.digits):
        """Return random string generator."""
        return ''.join(random.choice(chars) for x in range(size))