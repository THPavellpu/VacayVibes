from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main.views import home, category_packages, all_packages, book, subscribe, thank_you

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('destinations/<slug:category_slug>/', category_packages, name='category_packages'),
    path('packages/', all_packages, name='all_packages'),
    path('book/', book, name='book'),
    path('subscribe/', subscribe, name='subscribe'),
    path('thank-you/', thank_you, name='thank_you'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
