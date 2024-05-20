"""
Django command to wait to the database to be
available
"""

import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError  # type: ignore
from django.core.management.base import BaseCommand  # type: ignore


class Command(BaseCommand):
    """ Wait to the database to be available"""
    def handle(self, *args, **options):
        """entry point for coomand """
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('database is not available, waiting...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available'))
