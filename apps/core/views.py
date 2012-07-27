# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render,redirect

def home(request):
    return redirect('album:list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for registering, you can now login.')
            return HttpResponseRedirect(reverse('core:login'))
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, u'你已经成功退出.')
    return redirect('core:home')
