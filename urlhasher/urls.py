from django.urls import path

from .views import views

app_name = 'hasher'

urlpatterns = [
    path('', views.hash_url, name='hash-url'),
    path('click/<str:value>/', views.click_url, name='click_url'),
    path('privacy_click/<str:value>/', views.privacy_click_url, name='privacy_click_url')
]
