from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.signin, name="signin"),
    url(r'^to_login$', views.to_login, name="to_login"),
    url(r'^to_register$', views.to_register, name="to_register"),
    url(r'^profile/update_password/(?P<id>\d+)$', views.update_password, name="update_password"),
    url(r'^profile/to_update/(?P<id>\d+)$', views.to_update, name="to_update"),
    url(r'^logout$', views.logout, name="logout"),
]
