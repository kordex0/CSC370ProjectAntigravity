from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import User

@login_required
def user_profile(request):

    user = request.user.user

    return render(request, 'users/profile.html', {'user': user})
    
