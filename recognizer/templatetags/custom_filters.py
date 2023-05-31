from django import template
from recognizer.models import *

register = template.Library()

@register.filter
def get_type(value):
    return type(value).__name__