#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

from gitensite.apps.content.views import HomePageView
from gitensite.apps.content.views import NewsletterView
from gitensite.apps.content.views import SearchView
from gitensite.apps.content.views import BookPostView
from gitensite.apps.bookinfo.views import all_repos_txt
from gitensite.apps.bookinfo.views import metadata

#The secret must be stored in a file called "book-post-secret" located at the project root
secretfile = open("book-post-secret", "rw")
secret = secretfile.read()
secretfile.close()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/(?P<issue>\d)$', NewsletterView.as_view(), name='newsletter'),
    url(r'^updates/?$', TemplateView.as_view(template_name='updates.html'), name='updates'),
    url(r'^books/?$', SearchView.as_view(), name='books'),
    url(r'^search/?$', SearchView.as_view(), name='search'),
    url(r'^get-involved/?$', TemplateView.as_view(template_name='get-involved.html'), name='get-involved'),
    url(r'^faq/?$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^license/?$', TemplateView.as_view(template_name="license.html"), name='license'),
    url(r'^all_repos.txt$', all_repos_txt, name='all_repos.txt'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^books/(?P<book_id>\d+)\.(?P<ext>json|yaml)$', metadata, name='metadata'),
    url(r'^books/post/' + secret, BookPostView.as_view(), name='book-post')
]

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
