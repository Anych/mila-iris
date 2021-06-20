from time import time

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from uuslug import slugify


def gen_slug(obj, cat):
    """Generating slug field for new products"""
    new_slug = slugify(cat)
    obj = str(obj)
    new_slug2 = slugify(obj)
    return new_slug2 + '-' + new_slug + '-' + str(int(time()))
