from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.models import Product
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from home.sitemaps import StaticViewSitemap


sitemaps = {
    'blog': GenericSitemap({
        'queryset': Product.objects.all(),
        'date_field': 'date_added',
    }, priority=0.9),
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin-araik/', admin.site.urls),
    path('', include('home.urls')),

    path('sitemap.xml', sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


