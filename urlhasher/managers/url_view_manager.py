"""Manager file url view."""
import hashlib
from urlhasher.managers.url_manager import UrlManager


class UrlViewManager(object):
    """View manager of url."""

    def __init__(self) -> None:
        self.url_manager = UrlManager()

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
            
            return hash_value

        except Exception as e:
            return {'message': str(e)}
        


    def check_pre_existing_long_url(self, long_url):
        """Method to check the preexisting long_url."""
        url_obj = self.url_manager.load_by_long_url(long_url)

        if url_obj:
            return True
        
        return False
    
    def check_click_url(self, hash):
        """check the clicks of the url."""
        hashed_url_obj = self.url_manager.load_by_hash(hash)
        
        if hashed_url_obj is None:
            return None
        # increment the click count
        hashed_url_obj.clicks_remaining -= 1
        hashed_url_obj.save()

        return hashed_url_obj
    
    def check_number_of_click_available(self, hash):
        """check the remaining clicks."""
        hashed_url_obj = self.url_manager.load_by_hash(hash)
        if hashed_url_obj:

            if hashed_url_obj.clicks_remaining == 0:
                return False
            else:
              hashed_url_obj.clicks_remaining -= 1
              hashed_url_obj.save()  

        return hashed_url_obj
        


