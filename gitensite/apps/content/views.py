#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import View
from el_pagination.views import AjaxListView

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import F
from django.shortcuts import redirect

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

class EbookListingView(TemplateView):
    model = Book
    template_name = 'listing.html'

    def get_context_data(self, **kwargs):
        context = super(EbookListingView, self).get_context_data(**kwargs)

        results = Book.objects.filter(book_id=self.kwargs['bookid'])
        if len(results) > 0:
            matchedBook = results[0]
            context['book'] = matchedBook
            sameauthor = Book.objects.filter(author=matchedBook.author).order_by("title")
            context['sameauthor'] = sameauthor
        
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

class BookPostView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BookPostView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if ("CI" in os.environ and os.environ["CI"] == "true") or ("HTTP_X_GITENBERG_SECRET" in request.META and request.META["HTTP_X_GITENBERG_SECRET"] == os.environ["GITENBERG_SECRET"]):
            yaml = request.body
            addBookFromYaml(yaml)
            return HttpResponse("OK")
        else:
            return HttpResponse("Incorrect key or key not present", status=401)

class DownloadView(View):
    def get(self, request, bookid):
        results = Book.objects.filter(book_id=bookid)
        if len(results) > 0:
            matchedBook = results[0]

            matchedBook.num_downloads = F("num_downloads") + 1
            matchedBook.save()

            return redirect(matchedBook.downloads_url)

class BrowseBooksView(TemplateView):
    model = Book
    template_name = 'browsebooks.html'

    def get_context_data(self, **kwargs):
        context = super(BrowseBooksView, self).get_context_data(**kwargs)

        popular = Book.objects.filter(num_downloads__gt=0).order_by("-num_downloads")
        context["popular"] = popular[:12]

        recentlyadded = Book.objects.order_by("-added")
        context["recentlyadded"] = recentlyadded[:12]

        recentlyupdated = Book.objects.order_by("-updated")
        context["recentlyupdated"] = recentlyupdated[:12]
        
        return context