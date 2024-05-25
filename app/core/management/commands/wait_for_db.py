"""
Django command to wait to the database to be
available
"""

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError  
from django.core.management.base import BaseCommand 
from django.db import connection


class Command(BaseCommand):
    """ Wait to the database to be available"""
    def handle(self, *args, **options):
        """entry point for coomand """
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                #self.check(databases=['default'])
                connection.ensure_connection()
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('database is not available, waiting...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available'))
