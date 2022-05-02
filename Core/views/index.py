"""Core > views > index.py"""
# PYTHON IMPORTS
import logging
# DJANGO IMPORTS
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    """Landing page view"""
    template_name = 'index.html'
