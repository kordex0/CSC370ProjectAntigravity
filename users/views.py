from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import User, Admin, Teacher, Student

@login_required
def user_profile(request):

    # There should be a better way to do this. How to go from django user
    # to one of these users? Model function in User? Would that require
    # two lookups?
    user = None
    user_type = None
    try:
        user = Student.objects.get(django_user=request.user) 
        user_type = 'student'
    except Student.DoesNotExist:
        pass
    try:
        user = Admin.objects.get(django_user=request.user) 
        user_type = 'admin'
    except Admin.DoesNotExist:
        pass
    try:
        user = Teacher.objects.get(django_user=request.user) 
        user_type = 'teacher'
    except Teacher.DoesNotExist:
        pass

    return render(request, 'users/profile.html', {'user': user, 'user_type': user_type})
    
