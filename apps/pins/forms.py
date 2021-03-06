# -*- coding: utf-8 -*-
from django import forms

from .models import Pin,Album,Comment


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('name',)

class PinForm(forms.ModelForm):

    class Meta:
        model = Pin
        exclude = ['album']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
