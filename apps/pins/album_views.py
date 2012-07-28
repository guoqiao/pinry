# -*- coding: utf-8 -*-
import os
from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Album,Pin
from .forms import PinForm,AlbumForm

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

def list(request):
    objs = Album.objects.all()
    if not objs:
        x =  '还没有相册,登录后新建一个吧~'
        if request.user.is_authenticated():
            x =   '还没有相册,赶快新建一个吧~'
        messages.info(request,x)
    return render(request, 'pins/albums.html', {'objs':objs})

def home(request, pk):
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
    return TemplateResponse(request, 'pins/pins.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            messages.success(request, '新建相册成功')
            url = reverse('album:home', args=[a.id])
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Album did not pass validation!')
    else:
        form = AlbumForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'pins/new_album.html', context)

@login_required
def upload(request, pk):
    album = Album.objects.get(pk=pk)
    pin = Pin(album=album)
    if request.method == 'GET':
        if request.user != album.user:
            #messages.info(request,'注意:你可以上传照片,但只有相册的主人可以删除照片')
            pass
        form = PinForm(instance=pin)
    else:
        form = PinForm(request.POST, request.FILES, instance=pin)
        if form.is_valid():
            pin = form.save()
            data = [{
                'name': pin.file.name,
                'url': pin.file.url,
                'thumbnail_url': pin.file.url_200x1000,
                'delete_url': reverse('pin:delete', args=[pin.pk]),
                'delete_type': "DELETE",
                }]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    context = {'form': form, 'album': album}
    template = 'pins/pin_form.html'
    return render(request, template, context)

@login_required
def delete(request,pk):
    Album.objects.get(pk=pk).delete()
    url = reverse('album:list')
    return redirect(url)

def download(request,pk):
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

