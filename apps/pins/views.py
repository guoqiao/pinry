from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import redirect

from .models import Album
from .forms import PinForm,AlbumForm

def recent_albums(request):
    return TemplateResponse(request, 'pins/recent_albums.html', None)

def recent_pins(request, id):
    return TemplateResponse(request, 'pins/recent_pins.html', {'id':id})

def new_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            messages.success(request, 'New album successfully added.')
            url = reverse('pins:recent-pins', args=[a.id])
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Album did not pass validation!')
    else:
        form = AlbumForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'pins/new_album.html', context)

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

