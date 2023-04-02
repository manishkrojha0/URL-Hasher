"""Manager file url view."""
import hashlib
from urlhasher.managers import url_manager, url_short_manager


class UrlViewManager(object):
    """View manager of url."""

    def __init__(self) -> None:
        self.url_manager = url_manager.UrlManager()
        self.url_short_mgr = url_short_manager.UrlShortManager()

    def parse_and_hash_url(self, request_data):
        """Parse and hash url."""
        if request_data is None:
            return None
        try:
            long_url = request_data.get('long_url')
            # if self.check_pre_existing_long_url(long_url):
            #     raise Exception('Already hashed url and exhausted clicks.')
            utm_source = request_data.get('utm_source')
            utm_medium = request_data.get('utm_medium')
            utm_campaign = request_data.get('utm_campaign')
            hash_input = f'{long_url}-{utm_source}-{utm_medium}-{utm_campaign}'.encode()
            hash_value = hashlib.sha256(hash_input).hexdigest()
            self.url_manager.create(long_url=long_url,
                                    utm_source=utm_source,
                                    utm_medium=utm_medium,
                                    utm_campaign=utm_campaign,
                                    hash_value=hash_value,
                                    )
            
            
            url_short_obj = self.url_short_mgr.create_url_short(hash_value)

            return url_short_obj.value if url_short_obj else None

        except Exception as e:
            return {'message': str(e)}
        


    def check_pre_existing_long_url(self, long_url):
        """Method to check the preexisting long_url."""
        url_obj = self.url_manager.load_by_long_url(long_url)

        if url_obj:
            return True
        
        return False
    
    def check_click_url(self, value):
        """check the clicks of the url."""
        url_short_obj = self.url_short_mgr.load_by_value(value)
        if url_short_obj is None:
            return None
        hashed_url_obj = self.url_manager.load_by_id(url_short_obj.url.id)
        if hashed_url_obj is None:
            return None
        # decrement the click count
        hashed_url_obj.clicks_remaining -= 1
        hashed_url_obj.save()

        return hashed_url_obj
    
    def check_number_of_click_available(self, value):
        """check the remaining clicks."""
        url_short_obj = self.url_short_mgr.load_by_value(value)
        if url_short_obj is None:
            return None
        hashed_url_obj = self.url_manager.load_by_id(url_short_obj.url.id)
        if hashed_url_obj:

            if hashed_url_obj.clicks_remaining == 0:
                return False
            else:
              hashed_url_obj.clicks_remaining -= 1
              hashed_url_obj.save()  

        return hashed_url_obj
        


