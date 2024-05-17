"""
Django command to wait to the database to be
available
"""


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Wait to the database to be available"""

    def handle(self, *args, **options):
        pass