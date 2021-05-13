from django.urls import path
from .views import HomePage, contact, about, search_home

app_name = 'Home'

urlpatterns = [
    path('', HomePage, name='home'),
    path('about', about, name="about"),
    path('contact', contact, name="contact"),
    path('search', search_home, name="search_home"),
]
