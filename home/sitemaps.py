from django.contrib.sitemaps import Sitemap
import datetime


# STATIC DJANGO SITEMAP
class AbstractSitemapClass():
    changefreq = 'quarterly'
    url = None
    def get_absolute_url(self):
        return self.url


class StaticSitemap(Sitemap):
    pages = {
             'home':'/', #Add more static pages here like this 'example':'url_of_example',
             'contact':'/contact/',
             'portfolio':'/portfolio/',
             'resume':'/resume/',
        }
    main_sitemaps = []
    for page in pages.keys():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = pages[page]        
        main_sitemaps.append(sitemap_class)

    def items(self):
        return self.main_sitemaps    
    
    lastmod = datetime.datetime(2024, 7, 9)   #Enter the year,month, date you want in yout static page sitemap.
    priority = 1
    changefreq = "quarterly"   