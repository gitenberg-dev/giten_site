# from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Book

def all_repos_txt(request):
    response = StreamingHttpResponse(
        ['{}\t{}\r'.format(book.book_id,book.repo_url) for book in Book.objects.all()],
        content_type="text/csv")
    return response
    
def metadata(request, book_id, ext):
    book = get_object_or_404(Book, book_id=book_id )
    if ext=='yaml':
        return HttpResponse(book.yaml,content_type="text/x-yaml; charset=utf-8")
    else:
        return JsonResponse(book.metadata())
        
