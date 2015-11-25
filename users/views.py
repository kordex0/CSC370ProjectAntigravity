from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import User

@login_required
def user_profile(request):

    try:
        user = request.user.user
    
    except User.DoesNotExist:
        user = False #quick fix.
    
    return render(request, 'users/profile.html', {'user': user})
