"""Core > management > commands > wait_for_db.py"""
# PYTHON IMPORTS
import time
# DJANGO IMPORTS
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Command to pause execution until database is available"""

    def handle(self, *args, **options):
        """handler function"""
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write("Database not available, waiting 1 second..")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available"))
