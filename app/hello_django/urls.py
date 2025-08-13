from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main.views import welcome, about, statistics


urlpatterns = [
    path('', welcome, name='home'),  # Home page
    path('about/', about, name='about'),
    path('statistics/', statistics, name='statistics'),
    path('admin/', admin.site.urls),
]

# Removed media files configuration since upload functionality was removed
# if bool(settings.DEBUG):
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
