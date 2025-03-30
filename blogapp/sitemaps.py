from django.contrib.sitemaps import Sitemap
from .models import Blogs
from django.urls import reverse

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Blogs.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

#this ensures that static pages are optimized with SEO
class StaticPagesSitemap(Sitemap):
    changefred = "monthly"
    priority = 0.5

    def items(self):
        return['home', 'about', 'contact_us']

    def location(self, item):
        return reverse(item)

