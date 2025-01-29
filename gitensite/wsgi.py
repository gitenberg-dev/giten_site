"""
WSGI config for gitensite project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see

"""
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gitensite.settings')
os.environ.setdefault('ENVIRONMENT', 'NOT_PRODUCTION')
os.environ.setdefault('DJANGO_LOG', '/var/log/django/django.log')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
