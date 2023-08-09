from django.urls import path 
from . import views


urlpatterns = [
    path('', views.index,  kwargs = {'navbar': 'home'}),
    path('contact/', views.contact,  kwargs = {'navbar': 'contact'}),
    path('portfolio/', views.portfolio,  kwargs = {'navbar': 'portfolio'}),
    path('home/', views.index,  kwargs = {'navbar': 'home'}),
]