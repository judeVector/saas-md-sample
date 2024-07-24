from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
@login_required
def profile_view(request, username=None, *args, **kwargs):
    profile_user_obj = User.objects.get(username=username)
    return HttpResponse("Hello World")
