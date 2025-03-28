from django.urls import path
from . import views

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
]