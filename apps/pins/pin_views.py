# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from pins.models import Pin,Comment
from .forms import CommentForm

def home(request, pk):
    pin = Pin.objects.get(pk=pk)
    album = pin.album
    if request.method == 'GET':
        form = CommentForm()
    else:
        obj = Comment(user=request.user, pin=pin)
        form = CommentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('pin:home', pk=pk)

    ctx = {
        'album': album,
        'pin': pin,
        'form': form,
    }

    return render(request, 'pins/pin_home.html', ctx)

def nav(request, pk):
    pin = Pin.objects.get(pk=pk)
    album = pin.album
    direct = request.GET.get('direct','')
    pins = []
    if direct == 'prev':
        pins = Pin.objects.filter(album=album, pk__lt=pk).reverse()
    elif direct == 'next':
        pins = Pin.objects.filter(album=album, pk__gt=pk)
    if pins:
        pk = pins[0].pk
    return redirect('pin:home',pk=pk)

def rotate(request, pk):
    angle = request.GET.get('angle','0')
    angle = int(angle)
    if angle in (90,270):
        pin = Pin.objects.get(pk=pk)
        import Image
        path = pin.path()
        img0 = Image.open(path)
        img1 = img0.rotate(angle)
        img1.save(path)
    return redirect("pin:home", pk=pk)

@login_required
def delete(request,pk):
    pin = Pin.objects.get(pk=pk)
    album_id = pin.album.id
    pin.delete()
    return redirect('album:home', pk=album_id)
