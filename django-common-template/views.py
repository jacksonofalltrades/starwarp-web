from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import cardea.app
import logging
import hashlib

def home(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('/admin')
        else:
            return redirect('/account')
    else:
        return redirect('/pub')