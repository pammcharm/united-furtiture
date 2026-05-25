from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]
