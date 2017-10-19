#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from el_pagination.views import AjaxListView

from gitensite.apps.bookrepos.models import BookRepo
from gitensite.apps.bookinfo.models import Book

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

class UpdatesView(TemplateView):
    template_name = 'updates.html'

    def get_context_data(self, **kwargs):
        context = super(UpdatesView, self).get_context_data(**kwargs)
        return context

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

class GetInvolvedView(TemplateView):
    template_name = 'get-involved.html'

    def get_context_data(self, **kwargs):
        context = super(GetInvolvedView, self).get_context_data(**kwargs)
        return context

class FAQView(TemplateView):
    template_name = 'faq.html'

    def get_context_data(self, **kwargs):
        context = super(FAQView, self).get_context_data(**kwargs)
        return context