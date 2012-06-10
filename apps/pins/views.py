# -*- coding: utf-8 -*-
import os
from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import CreateView, DeleteView
from django.utils import simplejson
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Album,Pin
from .forms import PinForm,AlbumForm

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class PinCreateView(CreateView):
    model = Pin

    def dispatch(self, *args, **kwargs):
        self.album = get_object_or_404(Album, id=kwargs['id'])
        return super(PinCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PinCreateView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{
            'name': f.name, 
            'url': self.object.url(),
            'thumbnail_url': os.path.join(settings.MEDIA_URL, self.image.name),#TODO
            'delete_url': reverse('delete', args=[self.object.id]), 
            'delete_type': "DELETE",
        }]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PinDeleteView(DeleteView):
    model = Pin

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

def recent_albums(request):
    return TemplateResponse(request, 'pins/recent_albums.html', None)

def recent_pins(request, id):
    album = Album.objects.get(pk=id)
    return TemplateResponse(request, 'pins/recent_pins.html', {'album':album})

def new_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            messages.success(request, '新建相册成功')
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

def new_pin(request,id):
    album = Album.objects.get(id=id)
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.album = album
            pin.save()
            messages.success(request, '上传照片成功')
            return HttpResponseRedirect(reverse('pins:recent-pins', args=[id]))
        else:
            messages.error(request, 'Pin did not pass validation!')
    else:
        form = PinForm(initial={'album':album})
    context = {
        'form': form,
        'id': id,
    }
    return TemplateResponse(request, 'pins/new_pin.html', context)

