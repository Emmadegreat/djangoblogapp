from django.contrib.sitemaps import Sitemap
from .models import Blogs

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Blogs.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
