from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import User

@login_required
def user_profile(request):

    # There should be a better way to do this. How to go from django user
    # to one of these users? Model function in User? Would that require
    # two lookups?
    user = request.user.user
    user_type = user.get_roll_display()

    return render(request, 'users/profile.html', {'user': user, 'user_type': user_type})
    
