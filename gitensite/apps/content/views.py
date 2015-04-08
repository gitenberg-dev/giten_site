#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from gitensite.apps.bookrepos.models import BookRepo

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

class BookRepoListView(ListView):
    model = BookRepo
    template_name = 'bookrepo_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookRepoListView, self).get_context_data(**kwargs)

        return context

class GetInvolvedView(TemplateView):
    template_name = 'get-involved.html'

    def get_context_data(self, **kwargs):
        context = super(GetInvolvedView, self).get_context_data(**kwargs)
        return context