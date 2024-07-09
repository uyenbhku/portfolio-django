from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index,  kwargs = {'navbar': 'home'}),
    path('contact/', views.contact,  kwargs = {'navbar': 'contact'}),
    path('portfolio/', views.portfolio,  kwargs = {'navbar': 'portfolio'}),
    path('home/', views.index,  kwargs = {'navbar': 'home'}),
    path('resume/', views.pdf_view,  kwargs = {'navbar': 'resume'}),
    path('keep-alive/', views.keep_alive, name='keep-alive'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]