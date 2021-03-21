from accounts.views import Signup, Login, Logout
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path("signup", Signup, name="signup"),
    path("login", Login, name='login'),
    path("logout", Logout, name="logout"),
]
