from django.conf.urls import include, url
from django.contrib import admin

from gitensite.apps.content.views import HomePageView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
]
