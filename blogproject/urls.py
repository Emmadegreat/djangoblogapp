"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blogapp import views
from dashboard import views
from blogapp import views as Blogview
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import handler400, handler403, handler404 , handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blogapp.urls")),
    # path('category/', include("blogapp.urls")),
    path("<slug:slug>/", Blogview.Blogs, name = "blogs"),
    path("dashboard/", include("dashboard.urls"))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    handler400 = 'blogapp.views.bad_request'
    handler403 = 'blogapp.views.permission_denied'
    handler404 = 'blogapp.views.page_not_found'
    handler405 = 'blogapp.views.server_error'


