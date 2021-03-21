from django.urls import include, path
from django.contrib import admin

admin.site.site_header="Il Rifugio"
admin.site.site_title="Welcome to Il Rifugio Admin Panel"
admin.site.index_title="Il Rifugio Admin Pannel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Home.urls",namespace='Home'),name="Home"),
    path('accounts/', include('allauth.urls')),
    path("accounts/", include("accounts.urls",namespace='accounts'),name="accounts"),
    path("posts/", include("posts.urls",namespace='posts'),name="posts"),
    path('oauth/', include('social_django.urls', namespace='social')),
]
