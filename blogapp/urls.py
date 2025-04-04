from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSitemap, StaticPagesSitemap

sitemaps = {
    'blog' : BlogSitemap(),
    'staticpages' : StaticPagesSitemap()
}

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("category/<int:category_id>/", views.post_by_category, name="post_by_category"),
    path("posts/<slug:slug>/", views.single_blog, name="single_blog"), #note the posts before /<slug:slug> has nothing to do with our model or view
    path("blogs/search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("Logout/", views.Logout, name="Logout"),
    path("login/", views.login, name="login"),
    path("contact_us/", views.contact_us_view, name="contact_us"),
    path("contact_us_data/", views.contact_us_data_view, name="contact_us_data"),
    path("not_allowed/", views.not_allowed, name="not_allowed"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path("google1fc99727dbd27deb.html/", views.google_verification, name="google_verification"),
    path("sitemap.xml/", sitemap, {'sitemaps' : sitemaps}, name="sitemap"),

    #reset password urls
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    # path("social_auth", views.social_auth, name="social_auth"),
    # path("facebook", views.facebook_signin, name="facebook"),
    # path("google", views.google_signin, name="google"),
]