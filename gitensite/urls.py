#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

from gitensite.apps.content.views import HomePageView
from gitensite.apps.content.views import NewsletterView
from gitensite.apps.content.views import UpdatesView
from gitensite.apps.content.views import SearchView
from gitensite.apps.content.views import GetInvolvedView
from gitensite.apps.content.views import FAQView
from gitensite.apps.bookinfo.views import all_repos_txt
from gitensite.apps.bookinfo.views import metadata


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/(?P<issue>\d)$', NewsletterView.as_view(), name='newsletter'),
    url(r'^updates/?$', UpdatesView.as_view(), name='updates'),
    url(r'^books/?$', SearchView.as_view(), name='books'),
    url(r'^search/?$', SearchView.as_view(), name='search'),
    url(r'^get-involved/?$', GetInvolvedView.as_view(), name='get-involved'),
    url(r'^faq/?$', FAQView.as_view(), name='faq'),
    url(r'^license/?$', TemplateView.as_view(template_name="license.html"), name='license'),
    url(r'^all_repos.txt$', all_repos_txt, name='all_repos.txt'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^books/(?P<book_id>\d+)\.(?P<ext>json|yaml)$', metadata, name='metadata'),
]

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
