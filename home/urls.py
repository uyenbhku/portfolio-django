from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap


sitemaps = {
    'static': StaticSitemap, #add StaticSitemap to the dictionary
}

urlpatterns = [
    path('', views.index,  kwargs = {'navbar': 'home'}, name='home'),
    path('contact/', views.contact,  kwargs = {'navbar': 'contact'}, name='contact'),
    path('portfolio/', views.portfolio,  kwargs = {'navbar': 'portfolio'}, name='portfolio'),
    path('home/', views.index,  kwargs = {'navbar': 'home'}, name='home'),
    path('resume/', views.pdf_view,  kwargs = {'navbar': 'resume'}, name='resume'),
    path('keep-alive/', views.keep_alive, name='keep-alive'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]