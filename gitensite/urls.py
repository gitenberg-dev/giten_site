from django.conf.urls import include, url
from django.contrib import admin

from gitensite.apps.content.views import HomePageView
from gitensite.apps.content.views import NewsletterView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/(?P<issue>\d)$', NewsletterView.as_view(), name='newsletter'),
    url(r'^$', HomePageView.as_view(), name='home'),
]
