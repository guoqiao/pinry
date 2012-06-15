# -*- coding: utf-8 -*-
import os
from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import CreateView, DeleteView
from django.utils import simplejson
from django.shortcuts import render,redirect
from django.conf import settings

from .models import Album,Pin
from .forms import PinForm,AlbumForm

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

def upload_pin(request, pk):
    album = Album.objects.get(pk=pk)
    pin = Pin(album=album)
    if request.method == 'GET':
        form = PinForm(instance=pin)
    else:
        form = PinForm(request.POST, request.FILES, instance=pin)
        if form.is_valid():
            pin = form.save()
            data = [{
                'name': pin.file.name,
                'url': pin.file.url,
                'thumbnail_url': pin.file.url_200x1000,
                'delete_url': reverse('pins:delete-pin', args=[pin.pk]),
                'delete_type': "DELETE",
                }]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    context = {'form': form, 'album': album}
    template = 'pins/pin_form.html'
    return render(request, template, context)

def delete_pin(request,pk):
    pin = Pin.objects.get(pk=pk)
    album_id = pin.album.id
    pin.delete()
    url = reverse('pins:recent-pins', args=[album_id])
    return redirect(url)

def delete_album(request,pk):
    Album.objects.get(pk=pk).delete()
    url = reverse('pins:recent-albums')
    return redirect(url)

def download_album(request,pk):
    import zipfile
    obj = Album.objects.get(pk=pk)
    tarname = obj.name + '.zip'
    tarpath = os.path.join('/tmp/', tarname)
    tar = zipfile.ZipFile(tarpath, 'w')

    for pin in obj.pin_set.all():
        filename = pin.file.name # albums/1/a.jpg
        split = os.path.split(filename)
        tar.write(pin.path(), arcname=split[1])

    tar.close()

    fp = open(tarpath, 'rb')
    data = fp.read()
    fp.close()

    response = HttpResponse(data,mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % (tarname)
    return response

class PinCreateView(CreateView):
    model = Pin

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('image')
        data = [{
            'name': f.name, 
            'url': self.object.url(),
            'thumbnail_url': self.object.image.url(),
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
    objs = Album.objects.all()
    if not objs:
        x =  '还没有相册,登录后新建一个吧~'
        if request.user.is_authenticated():
            x =   '还没有相册,赶快新建一个吧~'
        messages.info(request,x)
    return TemplateResponse(request, 'pins/recent_albums.html', None)

def recent_pins(request, pk):
    album = Album.objects.get(pk=pk)
    if not album.pin_set.all():
        x =  '相册中还没有照片,登录后可以批量上传哦~'
        if request.user.is_authenticated():
            x = '相册中还没有照片,试试批量上传吧~'
        messages.info(request,x)

    context = {
        'album':album,
        'per_page': settings.API_LIMIT_PER_PAGE,
    }
    return TemplateResponse(request, 'pins/recent_pins.html', context)

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

def new_pin(request,pk):
    album = Album.objects.get(pk=pk)
    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.album = album
            pin.save()
            messages.success(request, '上传照片成功')
            return HttpResponseRedirect(reverse('pins:recent-pins', args=[pk]))
        else:
            messages.error(request, 'Pin did not pass validation!')
    else:
        form = PinForm(initial={'album':album})
    context = {
        'form': form,
        'pk': pk,
    }
    return TemplateResponse(request, 'pins/new_pin.html', context)

