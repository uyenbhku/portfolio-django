from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

from . import views
from .sitemaps import (
    StaticSitemap,
    # ProjectSitemap,
    # BlogSitemap,
    # TechnologySitemap
)

sitemaps = {
    'static': StaticSitemap,
    # 'projects': ProjectSitemap,
    # 'blog': BlogSitemap,
    # 'technologies': TechnologySitemap,
}

urlpatterns = [
    # Main pages
    path('', 
        views.HomeView.as_view(), 
        kwargs={'navbar': 'home'}, 
        name='home'
    ),
    path('about/', 
        views.AboutView.as_view(), 
        kwargs={'navbar': 'about'}, 
        name='about'
    ),
    path('contact/', 
        views.ContactView.as_view(), 
        kwargs={'navbar': 'contact'}, 
        name='contact'
    ),
    path('contact/success/', 
        TemplateView.as_view(
            template_name='pages/contact_success.html'
        ), 
        name='contact_success'
    ),
    
    # Portfolio
    path('portfolio/', 
        views.PortfolioView.as_view(), 
        kwargs={'navbar': 'portfolio'}, 
        name='portfolio'
    ),
    path('portfolio/<slug:slug>/', 
        views.ProjectDetailView.as_view(), 
        name='project_detail'
    ),
    
    # Blog
    path('blog/', 
        views.BlogListView.as_view(), 
        kwargs={'navbar': 'blog'}, 
        name='blog_list'
    ),
    path('blog/<slug:slug>/', 
        views.BlogDetailView.as_view(), 
        name='blog_detail'
    ),
    
    # Resume
    path('resume/', 
        cache_page(60 * 15)(views.resume_view), 
        name='resume'
    ),
    
    # Technologies
    # path('technologies/', 
    #     views.TechnologyListView.as_view(), 
    #     name='technology_list'
    # ),
    # path('technologies/<slug:slug>/', 
    #     views.TechnologyDetailView.as_view(), 
    #     name='technology_detail'
    # ),
    
    # SEO and utilities
    path('robots.txt',
        TemplateView.as_view(
            template_name="robots.txt",
            content_type='text/plain'
        ),
        name='robots'
    ),
    path('sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('.well-known/security.txt',
        TemplateView.as_view(
            template_name="security.txt",
            content_type='text/plain'
        ),
        name='security'
    ),
    
    # Health check
    path('health/', 
        views.keep_alive, 
        name='health-check'
    ),
]

handler404 = 'home.views.custom_404'
handler500 = 'home.views.custom_500'