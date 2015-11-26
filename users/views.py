from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import User
from courses.models import Section
from assignments.models import Assignment

@login_required
def user_profile(request):

    try:
        sections_list = []
        assignments_list = []
        user = request.user.user
        if user.is_teacher():
            sections_list = Section.objects.filter(teacher=user.id)
            return render(request, 'users/profile.html', {'user': user, 'sections_list': sections_list})
        elif user.is_student():
            sections_list = Section.objects.filter(students=user.id)
            for section in sections_list:
                assignments_list.extend(Assignment.objects.filter(section=section))
            print(assignments_list)
            return render(request, 'users/profile.html', {'user': user, 'sections_list': sections_list, 'assignments_list': assignments_list})
    except User.DoesNotExist:
        user = False #quick fix.
    return render(request, 'users/profile.html', {'user': user})
