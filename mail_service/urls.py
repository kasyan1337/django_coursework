from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mailing.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # home view
    path('mailing/', include('mailing.urls')),
    path('accounts/', include('allauth.urls')),  # This line includes the URL patterns provided by django-allauth.
    # These URL patterns handle user registration, login, logout, password reset, and other account-related operations.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)