#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from el_pagination.views import AjaxListView

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from gitensite.apps.bookrepos.models import BookRepo
from gitensite.apps.bookinfo.models import Book
from gitensite.apps.bookinfo.db import addBookFromYaml

import os

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

class NewsletterView(TemplateView):

    def get_template_names(self, **kwargs):
        return ['newsletters/{issue}.html'.format(
                issue=str(self.kwargs['issue'])
                )]

class SearchView(AjaxListView):
    model = Book
    template_name = 'book_list.html'
    page_template = 'book_list_page.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        return context

    def get_queryset(self):
        if self.request.GET.has_key('q'):
            return super(AjaxListView,self).get_queryset().filter(title__icontains=self.request.GET['q'])
        else:
            return super(AjaxListView,self).get_queryset()

class BookPostView(TemplateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BookPostView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if "HTTP_X_GITENBERG_SECRET" in request.META and request.META["HTTP_X_GITENBERG_SECRET"] == os.environ["GITENBERG_SECRET"]:
            yaml = request.body
            addBookFromYaml(yaml)
            return HttpResponse("OK")
        else:
            return HttpResponse("Incorrect key or key not present", status=401)
