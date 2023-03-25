from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseNotFound
from urlhasher.managers.url_view_manager import UrlViewManager
from django.urls import reverse




@csrf_exempt
def hash_url(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        url_view_mgr = UrlViewManager()
        hashed_url = url_view_mgr.parse_and_hash_url(data)
        return JsonResponse({
            'hashed_url': request.build_absolute_uri(reverse('hasher:click_url', args=[hashed_url]))
        })
    else:
        return JsonResponse({'message': "Please use post method."})

@csrf_exempt
def click_url(request, hashed_url):
    """Check for click of the users"""
    # get the hashed url object
    url_view_mgr = UrlViewManager()
    hashed_url_obj = url_view_mgr.check_click_url(hashed_url)

    if hashed_url_obj is None:
        return HttpResponseNotFound("non-existent hash value")
    
    # redirect to the original url
    return redirect('hasher:privacy_click_url', hashed_url=hashed_url)

@csrf_exempt
def privacy_click_url(request, hashed_url):
    """check the privacy clicks."""
    # get the hashed url object
    url_view_mgr = UrlViewManager()
    hashed_url_obj = url_view_mgr.check_number_of_click_available(hashed_url)
    
    # check if the hashed url has already been clicked
    if hashed_url_obj and hashed_url_obj.clicks_remaining > 0:
        # redirect to the original url
        return redirect(hashed_url_obj.long_url)
    elif hashed_url_obj is None:
        return HttpResponseNotFound("non-existent hash value")
    else:
        return JsonResponse({'message': 'This hashed URL has already been clicked and is no longer available for use.'})
