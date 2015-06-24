from django.contrib import admin
from .models import BookRepo
from .models import GitHubAuthToken

admin.site.register(BookRepo)
admin.site.register(GitHubAuthToken)
