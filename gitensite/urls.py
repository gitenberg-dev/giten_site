from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

from gitensite.apps.content.views import HomePageView
from gitensite.apps.content.views import NewsletterView
from gitensite.apps.content.views import BookRepoListView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/(?P<issue>\d)$', NewsletterView.as_view(), name='newsletter'),
    url(r'^books/?$', BookRepoListView.as_view(), name='books'),
    url(r'^$', HomePageView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
