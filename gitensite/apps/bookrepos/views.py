# from django.shortcuts import render
from django.http import HttpResponse
from .models import BookRepo

def all_repos_txt(request):
    return_str = ''
    for book in BookRepo.objects.all():
        return_str = return_str + '\n'
        return_str = return_str + book.html_url

    return HttpResponse(return_str, content_type='text/plain')
