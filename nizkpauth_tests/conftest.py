import django, os

from django.core.management import call_command

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nizkpauth_tests.settings')
    django.setup()
    call_command('migrate', 'core', 'zero')
    call_command('makemigrations', 'core')
    call_command('migrate', 'core')

