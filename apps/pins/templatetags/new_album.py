from django.template.loader import render_to_string
from django.template import Library

from pins.forms import AlbumForm


register = Library()


@register.simple_tag
def new_album():
    return render_to_string('pins/templatetags/new_album.html',
        {'form': AlbumForm()})
