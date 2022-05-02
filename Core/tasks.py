"""Core > tasks.py
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
# PYTHON IMPORTS
from __future__ import absolute_import, unicode_literals
import logging
# DJANGO IMPORTS
from django.core.management import call_command
from django.utils import timezone
# CELERY IMPORTS
from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def dbbackup(compress=1, clean=1, path=None, filename=None):
    """Backup database by calling the management command"""
    args = ['--noinput', ]
    kwargs = {}

    if compress > 0:
        args.append('--compress')
    if clean > 0:
        args.append('--clean')

    if path:
        kwargs.update({'output_path': path})
    if filename:
        kwargs.update({'output_filename': filename})

    try:
        call_command("dbbackup", *args, **kwargs)
        return f"{timezone.now()}: Database backup successful."
    except Exception as e:
        logger.error(e)
        return f"{timezone.now()} Could not backup database."
