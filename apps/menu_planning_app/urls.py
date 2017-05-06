from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^search$', views.search, name="search"),
  url(r'^search/(?P<count>\d+)$', views.to_search, name="to_search"),
  url(r'^favorite$', views.favorite, name="favorite"),
  url(r'^unfavorite$', views.unfavorite, name="unfavorite"),
  url(r'^profile/(?P<id>\d+)$', views.profile, name="profile"),
  url(r'^profile/update/(?P<id>\d+)$', views.update_profile, name="update_profile"),
  url(r'^recipe/(?P<id>\d+)$', views.recipe, name="recipe"),
]
