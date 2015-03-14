#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from django.shortcuts import render
from django.views.generic.base import TemplateView

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

