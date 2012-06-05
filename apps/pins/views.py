from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import PinForm,AlbumForm

def recent_pins(request):
    return TemplateResponse(request, 'pins/recent_pins.html', None)

def recent_albums(request):
    return TemplateResponse(request, 'pins/recent_albums.html', None)

def new_pin(request):
    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New pin successfully added.')
            return HttpResponseRedirect(reverse('pins:recent-pins'))
        else:
            messages.error(request, 'Pin did not pass validation!')
    else:
        form = PinForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'pins/new_pin.html', context)

def new_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New album successfully added.')
            return HttpResponseRedirect(reverse('pins:recent-albums'))
        else:
            messages.error(request, 'Album did not pass validation!')
    else:
        form = AlbumForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'pins/new_album.html', context)
