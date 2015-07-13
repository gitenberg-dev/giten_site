from django.contrib import admin
from .models import BookRepo
from .models import GitHubAuthToken
from .models import GHContributor

admin.site.register(BookRepo)
admin.site.register(GitHubAuthToken)
admin.site.register(GHContributor)
